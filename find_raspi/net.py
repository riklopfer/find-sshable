import dataclasses
import socket
from ipaddress import ip_network, IPv4Network, ip_address, IPv4Address
from typing import Optional, Dict, List, Iterable

import nmap3
import tqdm_thread


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


def find_sshable(network: Optional[IPv4Network] = None) -> Dict:
    """Find devices on given network with port 22 open. If no network is provided, use current network."""
    if network is None:
        network = get_network()

    nm_scan = nmap3.NmapScanTechniques()
    with tqdm_thread.tqdm_thread(desc="scanning for devices..."):
        return nm_scan.nmap_tcp_scan(network, args="--host-timeout 3 --open -p 22")


@dataclasses.dataclass
class Host:
    name: Optional[str]
    ip: IPv4Address

    @property
    def ip_str(self):
        return str(self.ip)


def _find_pi() -> Iterable[Host]:
    result = find_sshable()

    # pull these guys off
    stats = result.pop('stats', None)
    runtime = result.pop('runtime', None)

    # everything left is devices
    for ip, data in result.items():
        for hostname in data["hostname"]:
            if 'raspberrypi' in hostname["name"]:
                yield Host(name=hostname["name"], ip=ip_address(ip))


def find_pis(retries: Optional[int] = 1) -> List[Host]:
    assert retries > 0
    for _ in range(retries + 1):
        pi_addrs = list(_find_pi())
        if pi_addrs:
            return pi_addrs

    return []
