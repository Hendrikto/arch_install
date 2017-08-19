# author: Hendrik Werner <hendrik.to@gmail.com>

from typing import Iterable
from typing import Optional


class Adapter(object):
    @staticmethod
    def get_package_info(name: str) -> Optional[tuple]:
        raise NotImplementedError

    @staticmethod
    def install_packages(packages: Iterable) -> None:
        raise NotImplementedError
