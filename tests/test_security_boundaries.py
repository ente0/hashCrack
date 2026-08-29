from __future__ import annotations

import io
import os
import stat
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import functions


class SecurityBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.home = self.root / ".hashCrack"
        self.logs = self.home / "logs"
        self.home_patch = patch.object(functions, "HASHCRACK_HOME", self.home)
        self.logs_patch = patch.object(functions, "LOGS_DIR", self.logs)
        self.home_patch.start()
        self.logs_patch.start()

    def tearDown(self) -> None:
        self.logs_patch.stop()
        self.home_patch.stop()
        self.tempdir.cleanup()

    def test_session_validation_accepts_documented_names(self) -> None:
        for value in ("2026-08-27", "audit_2", "client.example-1"):
            self.assertEqual(functions.validate_session_name(value), value)

    def test_unique_session_suffix_remains_within_portable_limit(self) -> None:
        existing = self.root / "logs"
        existing.mkdir()
        long_name = "a" * 128
        (existing / long_name).mkdir()
        unique = functions.get_unique_session_name(long_name, str(existing))
        self.assertEqual(len(unique), 128)
        self.assertTrue(unique.endswith("_1"))
        self.assertEqual(functions.validate_session_name(unique), unique)

    def test_session_validation_rejects_traversal_and_shell_syntax(self) -> None:
        for value in (
            "",
            ".",
            "..",
            "../escape",
            "/absolute",
            "job;touch-pwned",
            "job&whoami",
            "line\nbreak",
            "CON",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                functions.validate_session_name(value)

    def test_windows_title_uses_data_api_and_preserves_printable_metacharacters(self) -> None:
        found = [{"plaintext": "pw&|><%^", "session": "safe"}]
        with patch.object(functions.sys, "platform", "win32"):
            with patch.object(functions, "_set_windows_console_title") as set_title:
                with patch.object(functions.os, "system") as shell:
                    functions.update_terminal_title("Windows", found)
        shell.assert_not_called()
        set_title.assert_called_once_with("hashCrack - pw&|><%^ (safe)")

    def test_posix_title_removes_embedded_terminal_controls(self) -> None:
        found = [{"plaintext": "secret\x07\x1b[31m", "session": "safe"}]
        output = io.StringIO()
        with patch.object(functions.sys, "platform", "linux"), redirect_stdout(output):
            functions.update_terminal_title("Linux", found)
        rendered = output.getvalue()
        self.assertEqual(rendered.count("\x1b"), 1)
        self.assertEqual(rendered.count("\x07"), 1)

    def test_restore_uses_exact_argv_and_never_a_shell(self) -> None:
        restore_root = self.root / "restore"
        restore_root.mkdir()
        valid = restore_root / "audit_1.restore"
        valid.write_text("state", encoding="utf-8")
        with patch.object(functions.subprocess, "run") as run:
            with patch.object(functions.os, "system") as shell:
                functions.restore_session(valid.name, str(restore_root))
        shell.assert_not_called()
        run.assert_called_once_with(
            ["hashcat", "--session=audit_1", "--restore"], check=False
        )

    def test_malicious_restore_filename_is_rejected(self) -> None:
        restore_root = self.root / "restore"
        restore_root.mkdir()
        malicious = restore_root / "job;touch-pwned.restore"
        malicious.write_text("state", encoding="utf-8")
        with patch.object(functions.subprocess, "run") as run:
            functions.restore_session(malicious.name, str(restore_root))
        run.assert_not_called()

    def test_malformed_restore_path_is_rejected_without_crashing(self) -> None:
        restore_root = self.root / "restore"
        restore_root.mkdir()
        (restore_root / "valid.restore").write_text("state", encoding="utf-8")
        malformed = "valid.restore/../inside.restore"
        with patch.object(functions.subprocess, "run") as run:
            functions.restore_session(malformed, str(restore_root))
        run.assert_not_called()

    def test_write_validates_existing_file_before_truncating(self) -> None:
        session_dir = self.logs / "audit"
        session_dir.mkdir(parents=True)
        target = session_dir / "status.json"
        target.write_text("keep", encoding="utf-8")
        original_check = functions._check_owned

        def reject_target(info, path):
            if Path(path) == target:
                raise PermissionError("controlled ownership rejection")
            return original_check(info, path)

        with patch.object(functions, "_check_owned", side_effect=reject_target):
            with self.assertRaises(PermissionError):
                functions.private_text_open(target, "w")
        self.assertEqual(target.read_text(encoding="utf-8"), "keep")

    def test_normal_private_write_still_truncates_after_validation(self) -> None:
        session_dir = self.logs / "audit"
        session_dir.mkdir(parents=True)
        target = session_dir / "status.json"
        target.write_text("old-data", encoding="utf-8")
        with functions.private_text_open(target, "w") as handle:
            handle.write("new")
        self.assertEqual(target.read_text(encoding="utf-8"), "new")

    @unittest.skipUnless(os.name == "posix", "FIFO semantics")
    def test_private_write_rejects_fifo_before_opening_it(self) -> None:
        session_dir = self.logs / "audit"
        session_dir.mkdir(parents=True)
        fifo = session_dir / "status.json"
        os.mkfifo(fifo)
        with self.assertRaises(RuntimeError):
            functions.private_text_open(fifo, "w")

    @unittest.skipUnless(os.name == "posix", "symlink semantics")
    def test_collect_status_rejects_symlinked_logs_root(self) -> None:
        external = self.root / "external-logs"
        session = external / "spoofed"
        session.mkdir(parents=True)
        (session / "status.json").write_text(
            '{"session":"spoofed","plaintext":"external-secret"}',
            encoding="utf-8",
        )
        self.home.mkdir()
        self.logs.symlink_to(external, target_is_directory=True)
        self.assertEqual(functions.collect_found_plaintexts(), [])
        self.assertEqual(functions.count_sessions(), 0)

    @unittest.skipUnless(os.name == "posix", "POSIX mode assertions")
    def test_sensitive_paths_are_owner_only_even_under_umask_022(self) -> None:
        previous = os.umask(0o022)
        try:
            plaintext, status_file, log_dir = functions.define_logs("audit")
            with functions.private_text_open(status_file, "w") as handle:
                handle.write("{}")
            with functions.private_text_open(Path(log_dir) / "hashcat.log", "w") as handle:
                handle.write("log")
        finally:
            os.umask(previous)

        for directory in (self.home, self.logs, Path(log_dir)):
            self.assertEqual(stat.S_IMODE(directory.stat().st_mode), 0o700)
        for sensitive in (Path(plaintext), Path(status_file), Path(log_dir) / "hashcat.log"):
            self.assertEqual(stat.S_IMODE(sensitive.stat().st_mode), 0o600)

    @unittest.skipUnless(os.name == "posix", "POSIX mode assertions")
    def test_existing_permissions_are_repaired_and_symlinks_rejected(self) -> None:
        session_dir = self.logs / "audit"
        session_dir.mkdir(parents=True, mode=0o755)
        status_file = session_dir / "status.json"
        status_file.write_text("{}", encoding="utf-8")
        status_file.chmod(0o644)

        functions.define_logs("audit")
        with functions.private_text_open(status_file, "a"):
            pass
        self.assertEqual(stat.S_IMODE(session_dir.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(status_file.stat().st_mode), 0o600)

        target = self.root / "target"
        target.write_text("secret", encoding="utf-8")
        link = session_dir / "command.txt"
        link.symlink_to(target)
        with self.assertRaises(RuntimeError):
            functions.private_text_open(link, "w")


if __name__ == "__main__":
    unittest.main()
