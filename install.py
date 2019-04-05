#!/usr/bin/env python3

# author: Hendrik Werner <hendrik.to@gmail.com>

from argparse import ArgumentParser
from backend.Adapter import Adapter
from backend.PacmanAdapter import PacmanAdapter
from backend.YaourtAdapter import YaourtAdapter
from backend.YayAdapter import YayAdapter


class Package():
    @classmethod
    def get_package(
        cls,
        name: str,
        adapter: Adapter,
    ):
        info = adapter.get_package_info(name)
        return cls(*info) if info else None

    def __init__(
        self,
        name: str,
        version: str,
        description: str,
        size: str,
        repo: str,
    ):
        self.name = name
        self.version = version
        self.description = description
        self.size = size
        self.repo = repo

    def __str__(self):
        return "\n".join([
            f" {self.name} ({self.version})",
            "╒" + "═" * (len(self.name) + len(self.version) + 3),
            f"├ size: {self.size}",
            f"├ repository: {self.repo}",
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
parser.add_argument(
    "-b", "--backend",
    type=str, default="pacman",
    choices=["pacman", "yaourt", "yay"],
    help="The package manager to be used as a backend."
)

args = parser.parse_args()

adapter = {
    "pacman": PacmanAdapter,
    "yaourt": YaourtAdapter,
    "yay": YayAdapter,
}[args.backend]

with open(args.file) as input_file:
    packages = input_file.read()
packages = [p.strip() for p in packages.splitlines()]
packages = [
    p for p in packages
    if p
    if not p.startswith("#")
]

candidates = []
for package_name in packages:
    package = Package.get_package(package_name, adapter)
    if package is None:
        continue
    print(f"\n{package}")
    if prompt("Install?"):
        candidates.append(package_name)

if not candidates:
    exit(0)

print(
    "\n",
    " Selected Packages\n",
    "╒═════════════════\n",
    "├ " + "\n├ ".join(candidates[:-1]) + "\n" if len(candidates) > 1 else "",
    "└ ", candidates[-1],
    sep="",
)

if prompt("Install selected packages?", default=False):
    adapter.install_packages(candidates)
