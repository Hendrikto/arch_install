#!/usr/bin/env python3

# author: Hendrik Werner <hendrik.to@gmail.com>


class Package():
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
