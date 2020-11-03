#!/usr/bin/env python3
import argparse
import ipaddress
import logging
import os
import re
import subprocess
import sys
from typing import Optional, Iterator, List

import sshconf


def get_ip_addr() -> ipaddress.IPv4Address:
  for dev in ['en0']:
    proc = subprocess.run(["ipconfig", "getifaddr", dev], capture_output=True)
    if proc.returncode == 0:
      ipaddr = proc.stdout.strip()
      if ipaddr:
        return ipaddress.ip_address(ipaddr.decode('utf8'))

  raise OSError("Could not find IP address! :(")


def get_network() -> ipaddress.IPv4Network:
  addr = get_ip_addr()
  net_str = str(addr)
  net_str = net_str[:net_str.rindex('.') + 1] + '0'
  net_str += '/24'
  return ipaddress.ip_network(net_str)


"""
Nmap scan report for 192.168.86.24
Host is up (0.021s latency).
Nmap scan report for philips-hue.lan (192.168.86.28)
"""
IP_RE = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
HOST_RE = r"\S+"
IP_PAT = re.compile(f"Nmap scan report for ({IP_RE})")
HOST_IP_PAT = re.compile(f"Nmap scan report for ({HOST_RE}) \(({IP_RE})\)")


class PiFinder(object):
  def __init__(self, local_ip: Optional[str] = None):
    if local_ip:
      self.local_network = local_ip
    else:
      self.local_network = get_network()
    self.logger.info("Using Local Network: %s", self.local_network)

  @property
  def logger(self):
    return logging.getLogger(self.__class__.__name__)

  def find_devices(self, ip_net: str):
    # All hosts
    # proc = subprocess.run(["nmap", "-sn", str(ip_net)], capture_output=True)
    # Only hosts with open ssh ports
    # nmap --host-timeout 3 --open -sT -p T:22 192.168.86.0/24
    proc = subprocess.run(
        ["nmap", "--host-timeout", "3", "--open", "-sT", "-p", "22",
         str(ip_net)],
        capture_output=True)
    # print(proc.stdout)
    out_str = proc.stdout.decode('utf8')
    self.logger.debug("nmap output:\n%s", out_str)
    for line in out_str.split('\n'):
      m = IP_PAT.match(line)
      if m:
        yield '', m.group(1)
      m = HOST_IP_PAT.match(line)
      if m:
        yield m.group(1), m.group(2)

  def find(self, retries=10) -> List[str]:
    for retry in range(retries):
      pi_addrs = list(self._find_all())
      if not pi_addrs:
        self.logger.info("No pi found... retrying %d/%d", retry + 1, retries)
        continue

      return pi_addrs

    raise AssertionError("Could not find raspberry pi!!!")

  def _find_all(self) -> Iterator[str]:
    name_ips = self.find_devices(f"{self.local_network}")
    for host, ip in name_ips:
      self.logger.debug("{:30}{:30}".format(host, ip))
      if 'raspberrypi' in host:
        yield ip


def main(argv):
  program_name = os.path.basename(argv[0])
  parser = argparse.ArgumentParser(prog=program_name)
  parser.add_argument('--name', '-n', help="HostName for the raspberry pi",
                      default='raspberrypi')
  parser.add_argument('-v', action='count', default=0)

  args = parser.parse_args(argv[1:])
  if args.v > 1:
    logging.basicConfig(level=logging.DEBUG)
  elif args.v > 0:
    logging.basicConfig(level=logging.INFO)
  else:
    logging.basicConfig(level=logging.WARNING)

  logger = logging.getLogger(program_name)
  pi_finder = PiFinder()
  pi_addrs = pi_finder.find()
  if len(pi_addrs) == 1:
    pi_names = [args.name]
  else:
    pi_names = [f"{args.name}-{idx + 1}" for idx in range(len(pi_addrs))]

  print(
      "Found {} Pi's... They will be added to your ssh config as follows\n"
      "{}".format(len(pi_addrs), "\n".join("\t".join(_)
                                           for _ in zip(pi_addrs, pi_names)))
  )

  # add it to your ssh config
  ssh_config_path = os.path.join(os.getenv("HOME", "/"), ".ssh", "config")
  if os.path.exists(ssh_config_path):
    config = sshconf.SshConfigFile(ssh_config_path)
  else:
    config = sshconf.empty_ssh_config_file()

  for addr, name in zip(pi_addrs, pi_names):
    host = config.host(name)
    ssh_config_kwargs = dict(host=name, User="pi", HostName=addr)
    logger.info("Updated ssh Host entry for %s", name)

    if host:
      logger.warning("Overwriting ssh config entry: %s", host)
      config.set(**ssh_config_kwargs)
    else:
      config.add(**ssh_config_kwargs)

  config.write(ssh_config_path)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
