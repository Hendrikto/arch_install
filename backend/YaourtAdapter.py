# author: Hendrik Werner <hendrik.to@gmail.com>

import re
import subprocess as sp
from backend.Adapter import Adapter
from typing import Iterable
from typing import Optional


class YaourtAdapter(Adapter):
    @staticmethod
    def get_package_info(name: str) -> Optional[tuple]:
        try:
            info = sp.run(
                ["yaourt", "-Si", name], stdout=sp.PIPE, check=True
            ).stdout.decode()
        except sp.CalledProcessError:
            return
        return (
            name,
            re.search("^Version\s*: (.*)$", info, re.MULTILINE)[1],
            re.search("^Description\s*: (.*)$", info, re.MULTILINE)[1],
            "unknown",
        )

    @staticmethod
    def install_packages(packages: Iterable) -> None:
        sp.run("yaourt -S --noconfirm".split() + packages)
