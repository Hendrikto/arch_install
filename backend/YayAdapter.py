# author: Hendrik Werner <hendrik.to@gmail.com>

import re
import subprocess as sp
from backend.Adapter import Adapter
from typing import Iterable
from typing import Optional


class YayAdapter(Adapter):
    @staticmethod
    def get_package_info(name: str) -> Optional[tuple]:
        try:
            info = sp.run(
                ["yay", "-Si", name], stdout=sp.PIPE, check=True
            ).stdout.decode()
        except sp.CalledProcessError:
            return
        installed_size = "unknown"
        if "Installed Size" in info:
            installed_size = re.search("^Installed Size\s*: (.*)$", info, re.MULTILINE)[1]
        return (
            name,
            re.search("^Version\s*: (.*)$", info, re.MULTILINE)[1],
            re.search("^Description\s*: (.*)$", info, re.MULTILINE)[1],
            installed_size,
            re.search("^Repository\s*: (.*)$", info, re.MULTILINE)[1],
        )

    @staticmethod
    def install_packages(packages: Iterable) -> None:
        sp.run(["yay", "-S", "--noconfirm"] + packages)
