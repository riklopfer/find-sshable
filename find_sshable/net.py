import dataclasses
import re
import socket
from ipaddress import ip_network, IPv4Network, ip_address, IPv4Address
from typing import Optional, Dict, List, Iterable

import nmap3
import tqdm_thread

from find_sshable import tools


def get_ip_addr() -> IPv4Address:
    hn = socket.gethostname()
    h = socket.gethostbyname(hn)
    return h


def get_network() -> IPv4Network:
    addr = get_ip_addr()
    pieces = str(addr).split('.')
    pieces[-1] = '0'
    net_str = f"{'.'.join(pieces)}/24"
    return ip_network(net_str)


def find_sshable(network: Optional[IPv4Network] = None, host_timeout: Optional[str] = None) -> Dict:
    """Find devices on given network with port 22 open. If no network is provided, use current network."""
    if network is None:
        network = get_network()

    if host_timeout is None:
        host_timeout = "3s"

    host_timeout = tools.simple_time_spec(host_timeout)

    nm_scan = nmap3.NmapScanTechniques()
    with tqdm_thread.tqdm_thread(desc="scanning for devices..."):
        return nm_scan.nmap_tcp_scan(network, args=f"--host-timeout {host_timeout} --open -p 22")


@dataclasses.dataclass
class Host:
    name: Optional[str]
    ip: IPv4Address

    @property
    def ip_str(self):
        return str(self.ip)


def _find_pi(host_timeout: Optional[str] = None,
             host_pattern: Optional[re.Pattern] = None) -> Iterable[Host]:
    result = find_sshable(host_timeout=host_timeout)

    # pull these guys off
    stats = result.pop('stats', None)
    runtime = result.pop('runtime', None)

    # everything left is devices
    for ip, data in result.items():
        for host_data in data["hostname"]:
            # if 'raspberrypi' in hostname["name"]:
            if host_pattern and not host_pattern.search(host_data["name"]):
                continue
            yield Host(name=host_data["name"], ip=ip_address(ip))


def find_hosts(retries: Optional[int] = 1,
               host_timeout: Optional[str] = None,
               host_pattern: Optional[re.Pattern] = None) -> List[Host]:
    assert retries > 0
    for _ in range(retries + 1):
        pi_addrs = list(_find_pi(host_timeout=host_timeout, host_pattern=host_pattern))
        if pi_addrs:
            return pi_addrs

    return []
