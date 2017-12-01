# author: Hendrik Werner <hendrik.to@gmail.com>

import re
import subprocess as sp
from backend.Adapter import Adapter
from typing import Iterable
from typing import Optional


class AuraAdapter(Adapter):
    @staticmethod
    def get_package_info(name: str) -> Optional[tuple]:
        try:
            info = sp.run(
                ["aura", "-Siq", name], stdout=sp.PIPE, check=True,
            ).stdout.decode()
            size = re.search("^Installed Size\s*: (.*)$", info, re.MULTILINE)[1]
        except sp.CalledProcessError:
            try:
                info = sp.run(
                    ["aura", "-Aiq", name], stdout=sp.PIPE, check=True,
                ).stdout.decode()
                size = "unknown"
            except sp.CalledProcessError:
                return
        return (
            name,
            re.search("^Version\s*: (.*)$", info, re.MULTILINE)[1],
            re.search("^Description\s*: (.*)$", info, re.MULTILINE)[1],
            size,
            re.search("^Repository\s*: (.*)$", info, re.MULTILINE)[1],
        )

    @staticmethod
    def install_packages(packages: Iterable) -> None:
        sp.run("aura -S --noconfirm".split() + packages)
