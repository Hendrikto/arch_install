#!/usr/bin/env python3

# author: Hendrik Werner <hendrik.to@gmail.com>

import re
import subprocess
from argparse import ArgumentParser


class Package():
    @classmethod
    def get_package(cls, name):
        try:
            info = subprocess.check_output(
                f"pacman -Qi {name}",
                shell=True,
            ).decode()
        except subprocess.CalledProcessError:
            return
        return cls(
            name=name,
            version=re.search("^Version\s*: (.*)$", info, re.MULTILINE)[1],
            description=re.search("^Description\s*: (.*)$", info, re.MULTILINE)[1],
            size=re.search("^Installed Size\s*: (.*)$", info, re.MULTILINE)[1]
        )

    def __init__(
        self,
        name: str,
        version: str,
        description: str,
        size: str,
    ):
        self.name = name
        self.version = version
        self.description = description
        self.size = size

    def __str__(self):
        return "\n".join([
            f" {self.name} ({self.version})",
            "╒" + "═" * (len(self.name) + len(self.version) + 3),
            f"├ size: {self.size}",
            f"└ description: {self.description}",
        ])


def prompt(
    message: str,
    start: str="::",
    default: bool=True,
) -> bool:
    indicator = "[Y/n]" if default else "[y/N]"
    choice = input(f"{start} {message} {indicator} ")
    if not choice:
        return default

    return choice.lower() in ["y", "yes"]


parser = ArgumentParser()
parser.description = "Interactively install a list of packages."
parser.add_argument(
    "file", nargs="?",
    type=str, default="packages.txt",
    help="A text file containing newline delimited package names.",
)

args = parser.parse_args()

with open(args.file) as input_file:
    packages = input_file.read()
packages = [
    p for p in packages.splitlines()
    if p
    if not p.startswith("#")
]

candidates = []
for package_name in packages:
    package = Package.get_package(package_name)
    if package is None:
        continue
    print(package)
    if prompt("Install?"):
        candidates.append(package_name)

if not candidates:
    exit(0)

print(
    "",
    " Selected Packages",
    "╒═════════════════",
    "├ " + "\n├ ".join(candidates[:-1]),
    "└ " + candidates[-1],
    sep="\n",
)

if prompt("Install selected packages?", default=False):
    subprocess.call("yes | sudo pacman -S " + " ".join(candidates), shell=True)
