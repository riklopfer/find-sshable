import dataclasses
import os
from typing import Optional, List

SSH_CONFIG_FILE = '~/.ssh/config'

DELIMITER = "#! managed by find_raspi modify with caution !#"

"""
#! managed by find_raspi modify with caution !#
Host raspberrypi.lan-0
  User pi
  HostName 192.168.86.20

Host raspberrypi.lan-1
  User pi
  HostName 192.168.86.36
#! managed by find_raspi modify with caution !#

Host xxxx
  HostName 192.32.54.5
  
"""


def _load_raspi(ifp) -> str:
    contents = ""
    for line in ifp:
        if line.startswith(DELIMITER):
            return contents
        contents += line


def load_config_parts(path: str) -> (str, str):
    raspi, other = "", ""
    with open(path, 'r', encoding='utf8') as ifp:
        for line in ifp:
            if line.startswith(DELIMITER):
                raspi = _load_raspi(ifp)
            else:
                other += line
    return raspi, other


@dataclasses.dataclass
class HostEntry:
    name: str
    User: Optional[str] = None
    HostName: Optional[str] = None

    def serialize(self) -> str:
        val = f"Host {self.name}\n"
        if self.User:
            val += f"    User {self.User}\n"
        if self.HostName:
            val += f"    User {self.HostName}\n"
        val += "\n"
        return val


def parse(string: str) -> List[HostEntry]:
    entries = []
    current = None
    for line in string.split("\n"):
        if line.startswith("Host"):
            if current:
                entries.append(current)
            current = HostEntry(line.split(" ")[-1])

        if line.strip().startswith("User"):
            current.User = line.split(" ")[-1]

        if line.strip().startswith("HostName"):
            current.HostName = line.split(" ")[-1]

    if current:
        entries.append(current)

    return entries


def serialize(entries: List[HostEntry]) -> str:
    val = DELIMITER + "\n"

    for entry in entries:
        val += entry.serialize()

    return val + DELIMITER


def get_rapi_hosts(config_path: Optional[str] = None) -> List[HostEntry]:
    if not config_path:
        config_path = os.path.expanduser(SSH_CONFIG_FILE)

    raspi, other = load_config_parts(config_path)

    return parse(raspi)


def update_rapi_hosts(entries: List[HostEntry], config_path: Optional[str] = None):
    if not config_path:
        config_path = os.path.expanduser(SSH_CONFIG_FILE)

    raspi, other = load_config_parts(config_path)

    with open(config_path, 'w', encoding='utf8') as ofp:
        ofp.write(other)
        for entry in entries:
            ofp.write(entry.serialize())
