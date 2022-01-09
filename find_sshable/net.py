import dataclasses
import re
import socket
from ipaddress import ip_network, IPv4Network, ip_address, IPv4Address
from typing import Optional, Dict, List

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


def is_sshable(target: str) -> bool:
    nmap = nmap3.Nmap()

    result = nmap.run_command(cmd=f"{nmap.nmaptool} -oX - -p 22 --script ssh-auth-methods {ip_address(target)}".split())
    et = nmap.get_xml_et(result)
    try:
        script_out = et.find("host").find("ports").find("port").find("script").get("output")
    except AttributeError:
        return False

    return (
            "Supported authentication methods:" in script_out and
            ("publickey" in script_out or "password" in script_out)
    )


def scan_open_port(host_timeout: Optional[str] = None, port: Optional[str] = "22") -> Dict:
    """Find devices on current network with port 22 open."""
    if host_timeout is None:
        host_timeout = "3s"

    host_timeout = tools.simple_time_spec(host_timeout)

    nm_scan = nmap3.NmapScanTechniques()
    with tqdm_thread.tqdm_thread(desc="scanning for devices..."):
        return nm_scan.nmap_tcp_scan(get_network(), args=f"--host-timeout {host_timeout} -T5 --open -p {port}")


@dataclasses.dataclass
class Host:
    name: Optional[str]
    ip: IPv4Address

    @property
    def ip_str(self):
        return str(self.ip)


def find_sshable(host_timeout: Optional[str] = None,
                 host_pattern: Optional[re.Pattern] = None,
                 passive: Optional[bool] = False) -> List[Host]:
    result = scan_open_port(host_timeout=host_timeout)

    # pull these guys off
    stats = result.pop('stats', None)
    runtime = result.pop('runtime', None)

    # everything left is devices
    hosts = []
    for ip, data in result.items():
        for host_data in data["hostname"]:
            if host_pattern and not host_pattern.search(host_data["name"]):
                continue
            if not passive and not is_sshable(ip):
                continue
            hosts.append(Host(name=host_data["name"], ip=ip_address(ip)))
    return hosts
