import subprocess
from ipaddress import ip_network, IPv4Network, ip_address, IPv4Address
from typing import Optional, Dict, List, Iterable

import nmap3


def get_ip_addr() -> IPv4Address:
    for dev in ['en0']:
        proc = subprocess.run(["ipconfig", "getifaddr", dev], capture_output=True)
        if proc.returncode == 0:
            ipaddr = proc.stdout.strip()
            if ipaddr:
                return ip_address(ipaddr.decode('utf8'))

    raise OSError("Could not find IP address! :(")


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
    return nm_scan.nmap_tcp_scan(network, args="--host-timeout 3 --open -p 22")


def _find_pi() -> Iterable[IPv4Address]:
    result = find_sshable()

    # pull these guys off
    stats = result.pop('stats', None)
    runtime = result.pop('runtime', None)

    # everything left is devices
    for ip, data in result.items():
        for hostname in data["hostname"]:
            if 'raspberrypi' in hostname["name"]:
                yield ip_address(ip)


def find_pis(retries: Optional[int] = 3) -> List[IPv4Address]:
    for _ in range(retries):
        pi_addrs = list(_find_pi())
        if pi_addrs:
            return pi_addrs

    raise ValueError("Raspberry PI not found!")
