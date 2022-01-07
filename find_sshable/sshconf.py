import dataclasses
import logging
import os
import shutil
from typing import Optional, List

SSH_CONFIG_FILE = '~/.ssh/config'

DELIMITER = "#! managed by find_sshable modify with caution !#"

logger = logging.getLogger(os.path.basename(__file__))


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
            val += f"    HostName {self.HostName}\n"
        val += "\n"
        return val


def _load_raspi(ifp) -> str:
    contents = ""
    for line in ifp:
        if line.startswith(DELIMITER):
            return contents
        contents += line


def _load_config_parts(path: str) -> (str, str):
    raspi, other = "", ""
    if os.path.exists(path):
        with open(path, 'r', encoding='utf8') as ifp:
            for line in ifp:
                if line.startswith(DELIMITER):
                    raspi = _load_raspi(ifp)
                else:
                    other += line
    return raspi.strip(), other.strip()


def _parse(string: str) -> List[HostEntry]:
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


def _serialize(entries: List[HostEntry]) -> str:
    val = "\n\n" + DELIMITER + "\n\n"

    for entry in entries:
        val += entry.serialize()

    return val + DELIMITER + "\n"


def get_raspi_hosts(config_path: Optional[str] = None) -> List[HostEntry]:
    if not config_path:
        config_path = os.path.expanduser(SSH_CONFIG_FILE)

    raspi, other = _load_config_parts(config_path)

    return _parse(raspi)


def update_raspi_hosts(entries: List[HostEntry],
                       config_path: Optional[str] = None,
                       backup: Optional[bool] = True):
    if not config_path:
        config_path = os.path.expanduser(SSH_CONFIG_FILE)

    if backup and os.path.exists(config_path):
        shutil.copy(config_path, f'{config_path}.bak')
        logger.debug("Made copy of ssh config %s", f"{config_path}.bak")

    raspi, other = _load_config_parts(config_path)

    with open(config_path, 'w', encoding='utf8') as ofp:
        ofp.write(other)
        ofp.write(_serialize(entries))
