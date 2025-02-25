from dataclasses import dataclass
from typing import List


@dataclass
class Deployment:
    __remote: str
    __local_path: str
    __identifier: str
    __branch: str
    __version_control: str = 'git'
    __run_scripts: List[str] = None

    @property
    def remote(self):
        return self.__remote

    @property
    def local_path(self):
        return self.__local_path

    @property
    def identifier(self):
        return self.__identifier

    @property
    def branch(self):
        return self.__branch

    @property
    def version_control(self):
        return self.__version_control

    @property
    def run_scripts(self):
        return self.__run_scripts or []  # Return empty list if None

    def __str__(self):
        return f"Deployment: {self.identifier} - {self.__remote} [{self.__branch}] - {self.__local_path}"
