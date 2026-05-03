"""Textual-based modern TUI for hashCrack.

Arrow-key / keyboard driven dashboard. Launches hashcat attacks through modal
forms and streams output live to a RichLog. The CLI-style scripts under
linux/ and windows/ remain usable for headless/scripted runs.
"""
from __future__ import annotations

import os
import re
import shlex
import subprocess
from pathlib import Path

from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Grid, Horizontal, VerticalScroll, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    Button, DataTable, Footer, Header, Input, Label, RichLog, Static, Switch,
)

from hashCrack.functions import (
    LOGS_DIR,
    clean_hashcat_cache,
    collect_found_plaintexts,
    count_sessions,
    define_default_parameters,
    define_logs,
    define_windows_parameters,
    get_potfile_info,
    save_logs,
)


ASCII_BANNER = (
    " ▄  █ ██      ▄▄▄▄▄    ▄  █ ▄█▄    █▄▄▄▄ ██   ▄█▄    █  █▀\n"
    "█   █ █ █    █     ▀▄ █   █ █▀ ▀▄  █  ▄▀ █ █  █▀ ▀▄  █▄█  \n"
    "██▀▀█ █▄▄█ ▄  ▀▀▀▀▄   ██▀▀█ █   ▀  █▀▀▌  █▄▄█ █   ▀  █▀▄  \n"
    "█   █ █  █  ▀▄▄▄▄▀    █   █ █▄  ▄▀ █  █  █  █ █▄  ▄▀ █  █ \n"
    "   █     █               █  ▀███▀    █      █ ▀███▀    █  \n"
    "  ▀     █               ▀           ▀      █          ▀   \n"
    "       ▀                                  ▀               "
)


def _stat_content(label: str, value: str, color: str = "cyan") -> str:
    return f"[bold {color}]{label}[/]\n{value}"


def _hash_file_markup(hash_file: str | None) -> str:
    if hash_file and os.path.isfile(hash_file) and os.path.getsize(hash_file) > 0:
        try:
            with open(hash_file, "r", encoding="utf-8", errors="replace") as f:
                preview = f.readline().strip()
            preview = preview[:60] + "..." if len(preview) > 60 else preview
            return (
                f"[green]✓ Hash:[/] [bold]{os.path.basename(hash_file)}[/] "
                f"[dim]({os.path.getsize(hash_file)} B)[/]\n"
                f"[dim]path:[/]    {hash_file}\n"
                f"[dim]preview:[/] {preview}"
            )
        except Exception as e:
            return f"[yellow]! {hash_file}: unreadable ({e})[/]"
    if hash_file:
        return f"[red]✕ {hash_file}: file not found or empty[/]"
    return "[red]✕ No hash file loaded[/]"


# --------------------------------------------------------------------------- #
#   Attack form modal
# --------------------------------------------------------------------------- #

class AttackFormScreen(ModalScreen[dict]):
    """Modal form for configuring an attack. Returns the dict of inputs on Run, None on cancel."""

    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    ATTACK_TITLES = {
        "wordlist":   "Wordlist attack (-a 0)",
        "rule":       "Wordlist + Rules attack (-a 0 -r)",
        "bruteforce": "Brute-force mask attack (-a 3)",
        "combo":      "Combinator attack: wordlist + mask (-a 6)",
    }

    def __init__(self, attack_type: str, params: dict, os_name: str, force_default: bool):
        super().__init__()
        self.attack_type = attack_type
        self.params = params
        self.os_name = os_name
        self.force_default = force_default

    def compose(self) -> ComposeResult:
        p = self.params
        a = self.attack_type
        with Container(id="form_dialog"):
            yield Static(f"[bold cyan]{self.ATTACK_TITLES[a]}[/]  [dim]— {self.os_name}[/]", id="form_title")
            with VerticalScroll(id="form_body"):
                yield Label("Session name")
                yield Input(value=p["default_session"], id="f_session")

                yield Label("Hash mode (-m)")
                yield Input(value=p["default_hashmode"], id="f_hashmode")

                if a in ("wordlist", "rule", "combo"):
                    yield Label("Wordlists path")
                    yield Input(value=p["default_wordlists"], id="f_wordlist_path")
                    yield Label("Wordlist filename")
                    yield Input(value=p["default_wordlist"], id="f_wordlist")

                if a == "rule":
                    yield Label("Rules path")
                    yield Input(value=p["default_rules"], id="f_rule_path")
                    yield Label("Rule filename")
                    yield Input(value=p["default_rule"], id="f_rule")

                if a in ("bruteforce", "combo"):
                    yield Label("Mask")
                    yield Input(value=p["default_mask"], id="f_mask")
                    yield Label("Min length (--increment-min)")
                    yield Input(value=p["default_min_length"], id="f_min_length")
                    yield Label("Max length (--increment-max)")
                    yield Input(value=p["default_max_length"], id="f_max_length")

                yield Label("Workload [1-4]")
                yield Input(value=p["default_workload"], id="f_workload")
                yield Label("Device")
                yield Input(value=p["default_device"], id="f_device")

                with Horizontal(classes="switch_row"):
                    yield Label("Status timer")
                    yield Switch(value=p["default_status_timer"].lower() == "y", id="f_status_timer")
                with Horizontal(classes="switch_row"):
                    yield Label("[bold red]--force[/]")
                    yield Switch(value=self.force_default, id="f_force")

            with Horizontal(id="form_buttons"):
                yield Button("Run", variant="success", id="btn_run")
                yield Button("Cancel", variant="default", id="btn_cancel")

    def action_cancel(self) -> None:
        self.dismiss(None)

    @on(Button.Pressed, "#btn_cancel")
    def _on_cancel(self) -> None:
        self.dismiss(None)

    @on(Button.Pressed, "#btn_run")
    def _on_run(self) -> None:
        result = {"attack_type": self.attack_type}
        for w in self.query(Input):
            if w.id and w.id.startswith("f_"):
                result[w.id[2:]] = w.value
        for w in self.query(Switch):
            if w.id and w.id.startswith("f_"):
                result[w.id[2:]] = w.value
        self.dismiss(result)


# --------------------------------------------------------------------------- #
#   Run screen (live hashcat output)
# --------------------------------------------------------------------------- #

class RunScreen(Screen):
    """Spawn hashcat in a worker thread and stream its output to a RichLog."""

    BINDINGS = [
        Binding("ctrl+c", "stop",  "Stop"),
        Binding("escape", "back",  "Back to menu"),
    ]

    # Matches hashcat's "Status.........: Cracked" line (any number of dots)
    _STATUS_CRACKED = re.compile(r"Status\.+:\s*Cracked", re.IGNORECASE)

    def __init__(self, cmd: list[str], session: str, save_kwargs: dict):
        super().__init__()
        self.cmd = cmd
        self.session = session
        self.save_kwargs = save_kwargs
        self.proc: subprocess.Popen | None = None
        self._finished = False
        self._hashcat_cracked = False

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Static(f"[bold]Session[/] {self.session}    [dim]ctrl+c: stop · esc: back[/]", id="run_header")
        yield Static(" ".join(shlex.quote(c) for c in self.cmd), id="run_cmd")
        yield RichLog(id="run_log", highlight=False, markup=False, auto_scroll=True, wrap=False)
        yield Footer()

    def on_mount(self) -> None:
        self._run_hashcat()

    @work(thread=True, exclusive=True)
    def _run_hashcat(self) -> None:
        log = self.query_one(RichLog)
        _pt, _st, log_dir = define_logs(self.session)
        hashcat_log = os.path.join(log_dir, "hashcat.log")
        try:
            with open(hashcat_log, "w", encoding="utf-8") as logf:
                self.proc = subprocess.Popen(
                    self.cmd,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, bufsize=1,
                )
                assert self.proc.stdout is not None
                for line in self.proc.stdout:
                    stripped = line.rstrip()
                    self.app.call_from_thread(log.write, stripped)
                    logf.write(line)
                    if self._STATUS_CRACKED.search(stripped):
                        self._hashcat_cracked = True
                self.proc.wait()
        except FileNotFoundError:
            self.app.call_from_thread(log.write, "Error: 'hashcat' binary not found in PATH.")
        self.app.call_from_thread(self._finish)

    def _finish(self) -> None:
        if self._finished:
            return
        self._finished = True
        save_logs(
            self.session,
            command=" ".join(shlex.quote(c) for c in self.cmd),
            silent=True,
            **self.save_kwargs,
        )
        log = self.query_one(RichLog)

        plaintext_file, _status_file, _log_dir = define_logs(self.session)
        plaintext = None
        if os.path.exists(plaintext_file) and os.path.getsize(plaintext_file) > 0:
            try:
                with open(plaintext_file, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            plaintext = line
                            break
            except Exception:
                plaintext = None

        cracked = self._hashcat_cracked or bool(plaintext)

        log.write("")
        if cracked:
            log.write(Text("  ✓ CRACKED", style="bold cyan"))
            if plaintext:
                log.write(Text(f"  Plaintext : {plaintext}", style="bold white"))
            log.write(Text("  status.json saved", style="dim"))
        else:
            log.write(Text("  ✕ Hash not cracked", style="bold red"))
            log.write(Text("  status.json saved", style="dim"))

    def action_stop(self) -> None:
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()

    def action_back(self) -> None:
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.app.pop_screen()


# --------------------------------------------------------------------------- #
#   Status / cracked sessions screen
# --------------------------------------------------------------------------- #

class StatusScreen(Screen):
    BINDINGS = [Binding("escape", "back", "Back")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("[bold green]Cracked sessions[/]", id="status_title")
        yield DataTable(id="found_table", zebra_stripes=True)
        yield Footer()

    def on_mount(self) -> None:
        t = self.query_one(DataTable)
        t.cursor_type = "row"
        t.add_columns("Session", "Plaintext", "Attack", "Wordlist", "Rule", "Mask")
        rows = collect_found_plaintexts()
        if not rows:
            t.add_row("-", "(no plaintexts found)", "-", "-", "-", "-")
            return
        for p in rows:
            t.add_row(
                p["session"],
                p["plaintext"],
                p.get("attack") or "-",
                str(p.get("wordlist") or "-"),
                str(p.get("rule") or "-"),
                str(p.get("mask") or "-"),
            )

    def action_back(self) -> None:
        self.app.pop_screen()


# --------------------------------------------------------------------------- #
#   Main menu / dashboard
# --------------------------------------------------------------------------- #

class MenuScreen(Screen):
    BINDINGS = [
        Binding("1",      "attack('wordlist')",   "Wordlist"),
        Binding("2",      "attack('rule')",       "Rule"),
        Binding("3",      "attack('bruteforce')", "Brute"),
        Binding("4",      "attack('combo')",      "Combo"),
        Binding("5",      "show_status",          "Status"),
        Binding("c",      "clear_potfile",        "Clear potfile"),
        Binding("x",      "toggle_os",            "Switch OS"),
        Binding("q",      "quit_app",             "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Static(ASCII_BANNER, id="banner")
        with Grid(id="stats_grid"):
            yield Static(_stat_content("OS",       self.app.os_name),      id="stat_os",      classes="stat_card")
            yield Static(_stat_content("Potfile",  self._potfile_str()),   id="stat_pot",     classes="stat_card")
            yield Static(_stat_content("Sessions", str(count_sessions())), id="stat_sess",    classes="stat_card")
            yield Static(_stat_content("Cracked",  str(len(collect_found_plaintexts()))), id="stat_cracked", classes="stat_card")
        yield Static(_hash_file_markup(self.app.hash_file), id="hash_panel")
        with Vertical(id="attacks_panel"):
            yield Static("[bold cyan]Attack modes[/]", classes="section_title")
            yield Static("[cyan][1][/] Wordlist                    [dim]hashcat -a 0 <wordlist>[/]              [blue]EASY[/]")
            yield Static("[cyan][2][/] Wordlist + Rules            [dim]hashcat -a 0 <wordlist> -r <rule>[/]    [green]MEDIUM[/]")
            yield Static("[cyan][3][/] Brute-Force (mask)          [dim]hashcat -a 3 <mask> --increment[/]      [yellow]HARD[/]")
            yield Static("[cyan][4][/] Combinator (wordlist+mask)  [dim]hashcat -a 6 <wordlist> <mask>[/]       [red]ADVANCED[/]")
            yield Static("[cyan][5][/] Plaintext status            [dim]inspect cracked sessions[/]")
            yield Static("")
            yield Static("[magenta][C][/] Clear potfile     [magenta][X][/] Switch OS     [magenta][Q][/] Quit", classes="utils_row")
        yield Footer()

    def _potfile_str(self) -> str:
        path, size = get_potfile_info()
        return f"{size:,} B" if path else "none"

    def _refresh_dashboard(self) -> None:
        self.query_one("#stat_os",      Static).update(_stat_content("OS",       self.app.os_name))
        self.query_one("#stat_pot",     Static).update(_stat_content("Potfile",  self._potfile_str()))
        self.query_one("#stat_sess",    Static).update(_stat_content("Sessions", str(count_sessions())))
        self.query_one("#stat_cracked", Static).update(_stat_content("Cracked",  str(len(collect_found_plaintexts()))))
        self.query_one("#hash_panel",   Static).update(_hash_file_markup(self.app.hash_file))

    def action_attack(self, attack_type: str) -> None:
        if not (self.app.hash_file and os.path.isfile(self.app.hash_file) and os.path.getsize(self.app.hash_file) > 0):
            self.app.bell()
            self.app.notify("Hash file missing or empty; cannot launch attack.", severity="error")
            return
        params = self.app.get_params()

        def _after_form(result):
            if not result:
                return
            cmd, save_kwargs = self.app.build_command(attack_type, result)
            if cmd is None:
                return
            session = result.get("session") or params["default_session"]
            self.app.push_screen(RunScreen(cmd, session, save_kwargs))

        self.app.push_screen(
            AttackFormScreen(attack_type, params, self.app.os_name, self.app.force_default),
            _after_form,
        )

    def action_show_status(self) -> None:
        self.app.push_screen(StatusScreen())

    def action_toggle_os(self) -> None:
        self.app.os_name = "Windows" if self.app.os_name == "Linux" else "Linux"
        self._refresh_dashboard()
        self.app.notify(f"Switched to {self.app.os_name}")

    def action_clear_potfile(self) -> None:
        removed, err = clean_hashcat_cache(verbose=False)
        self._refresh_dashboard()
        if err:
            self.app.notify(f"Potfile cleanup failed: {err}", severity="error")
        elif removed:
            self.app.notify(f"Cleared {len(removed)} potfile(s)")
        else:
            self.app.notify("No potfile found", severity="warning")

    def action_quit_app(self) -> None:
        self.app.exit()


# --------------------------------------------------------------------------- #
#   Root app
# --------------------------------------------------------------------------- #

class HashCrackApp(App):
    TITLE = "hashCrack"
    SUB_TITLE = "hashcat TUI"

    CSS = """
    Screen {
        background: $surface;
    }
    #banner {
        color: $accent;
        text-align: center;
        padding: 1 0;
        text-style: bold;
    }
    #stats_grid {
        grid-size: 4 1;
        grid-columns: 1fr 1fr 1fr 1fr;
        grid-gutter: 1;
        padding: 0 2;
        height: 5;
    }
    .stat_card {
        border: round $accent;
        padding: 0 1;
        content-align: center middle;
        text-align: center;
    }
    #hash_panel {
        border: round $success;
        padding: 1 2;
        margin: 1 2 0 2;
    }
    #attacks_panel {
        border: round $accent;
        padding: 1 2;
        margin: 1 2;
    }
    .section_title {
        padding: 0 0 1 0;
    }
    .utils_row {
        padding-top: 1;
        color: $warning;
    }
    #run_header {
        padding: 0 2;
        color: $text;
        background: $primary-background;
    }
    #run_cmd {
        padding: 0 2;
        color: $accent;
        text-style: bold;
    }
    #run_log {
        border: round $accent;
        margin: 1 2;
        height: 1fr;
    }
    AttackFormScreen {
        align: center middle;
    }
    #form_dialog {
        width: 95%;
        max-width: 90;
        height: 95%;
        max-height: 40;
        border: thick $accent;
        background: $surface;
        padding: 1 2;
    }
    #form_title {
        padding: 0 0 1 0;
    }
    #form_body {
        height: 1fr;
    }
    #form_body Label {
        padding: 1 0 0 0;
        color: $text-muted;
    }
    .switch_row {
        height: 3;
        padding: 1 0 0 0;
    }
    .switch_row Label {
        padding: 0 2 0 0;
        width: 30;
    }
    #form_buttons {
        padding: 1 0 0 0;
        align: center middle;
        height: 3;
    }
    #status_title {
        padding: 1 2;
    }
    #found_table {
        margin: 0 2;
    }
    """

    def __init__(self, hash_file: str, os_name: str = "Linux", force_default: bool = False):
        super().__init__()
        self.hash_file = hash_file
        self.os_name = os_name
        self.force_default = force_default

    def on_mount(self) -> None:
        self.push_screen(MenuScreen())

    def get_params(self) -> dict:
        return define_windows_parameters() if self.os_name == "Windows" else define_default_parameters()

    def build_command(self, attack_type: str, form: dict):
        p = self.get_params()
        session   = form.get("session")     or p["default_session"]
        hashmode  = form.get("hashmode")    or p["default_hashmode"]
        workload  = form.get("workload")    or p["default_workload"]
        device    = form.get("device")      or p["default_device"]
        status_on = bool(form.get("status_timer"))
        force_on  = bool(form.get("force"))

        plaintext_path, _s, _d = define_logs(session)
        binary = f"{p['default_hashcat']}/hashcat.exe" if self.os_name == "Windows" else "hashcat"

        base = [
            binary,
            f"--session={session}",
            "-m", hashmode,
            self.hash_file,
            "-w", workload,
            "--outfile-format=2",
            "-o", plaintext_path,
            "-d", device,
            "--potfile-disable",
        ]

        save_kwargs = dict(
            hash_file=self.hash_file,
            attack_type=attack_type,
            hashmode=hashmode,
            workload=workload,
            device=device,
            force=force_on,
            os_name=self.os_name,
        )

        if attack_type == "wordlist":
            wl_path = form.get("wordlist_path") or p["default_wordlists"]
            wl      = form.get("wordlist")      or p["default_wordlist"]
            cmd = base + ["-a", "0", f"{wl_path}/{wl}"]
            save_kwargs.update(wordlist_path=wl_path, wordlist=wl)

        elif attack_type == "rule":
            wl_path = form.get("wordlist_path") or p["default_wordlists"]
            wl      = form.get("wordlist")      or p["default_wordlist"]
            r_path  = form.get("rule_path")     or p["default_rules"]
            r       = form.get("rule")          or p["default_rule"]
            cmd = base + ["-a", "0", f"{wl_path}/{wl}", "-r", f"{r_path}/{r}"]
            save_kwargs.update(wordlist_path=wl_path, wordlist=wl, rule_path=r_path, rule=r)

        elif attack_type == "bruteforce":
            mask = form.get("mask")       or p["default_mask"]
            mn   = form.get("min_length") or p["default_min_length"]
            mx   = form.get("max_length") or p["default_max_length"]
            cmd = base + ["-a", "3", mask, "--increment",
                          f"--increment-min={mn}", f"--increment-max={mx}"]
            save_kwargs.update(mask=mask, min_length=mn, max_length=mx)

        elif attack_type == "combo":
            wl_path = form.get("wordlist_path") or p["default_wordlists"]
            wl      = form.get("wordlist")      or p["default_wordlist"]
            mask    = form.get("mask")          or p["default_mask"]
            mn      = form.get("min_length")    or p["default_min_length"]
            mx      = form.get("max_length")    or p["default_max_length"]
            cmd = base + ["-a", "6", f"{wl_path}/{wl}", mask, "--increment",
                          f"--increment-min={mn}", f"--increment-max={mx}"]
            save_kwargs.update(wordlist_path=wl_path, wordlist=wl, mask=mask,
                               min_length=mn, max_length=mx)
        else:
            return None, None

        if status_on:
            cmd += ["--status", "--status-timer=2"]
        if force_on:
            cmd.append("--force")

        return cmd, save_kwargs


def launch(hash_file: str, os_name: str = "Linux", force_default: bool = False) -> None:
    """Entry point used by hashCrack.main()."""
    HashCrackApp(hash_file=hash_file, os_name=os_name, force_default=force_default).run()
