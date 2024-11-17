from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="hashCrack",
    version="1.1",
    description="A tool for hash cracking with additional utilities",
    #author="Your Name",
    #author_email="your.email@example.com",
    license="GPL-3.0",
    packages=find_packages(include=["scripts", "scripts.*"]),
    py_modules=["hashCrack", "check_dependencies", "functions"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "hashcrack=hashCrack:main",
        ]
    },
    include_package_data=True,
    package_data={
        "": ["wordlists.txt"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
