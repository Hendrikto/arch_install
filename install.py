#!/usr/bin/env python3

# author: Hendrik Werner <hendrik.to@gmail.com>

import re
import subprocess


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
