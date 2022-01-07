#!/usr/bin/env python3
import argparse
import collections
import logging
import os
import sys
from typing import Iterable, List

from find_raspi import net, sshconf

logger = logging.getLogger(os.path.basename(__file__))


def _update_names(hosts: List[net.Host]) -> List[net.Host]:
    name_count = collections.Counter()

    updated = []
    for host in hosts:
        updated.append(net.Host(name=f"{host.name}-{name_count[host.name]}", ip=host.ip))
        name_count[host.name] += 1

    return updated


def add_to_ssh_conf(hosts: Iterable[net.Host]):
    if hosts is not None:
        hosts = list(hosts)

    assert hosts, "Addrs is empty"

    hosts = _update_names(hosts)

    print(
        "\nPi's will be added to your ssh config as follows\n"
        "{}".format("\n".join("\t".join([h.name, str(h.ip)])
                              for h in hosts))
    )

    # add it to your ssh config
    ssh_config_path = os.path.join(os.getenv("HOME", "/"), ".ssh", "config")

    host_entries = [sshconf.HostEntry(h.name, User="pi", HostName=h.ip_str) for h in hosts]
    sshconf.update_raspi_hosts(host_entries, ssh_config_path)


def main(argv):
    program_name = os.path.basename(argv[0])
    parser = argparse.ArgumentParser(prog=program_name)
    parser.add_argument('--update-ssh-config',
                        help="Update ssh config with entries for the raspberry pi hosts",
                        action='store_true')
    parser.add_argument('--retries', '-r',
                        help="Number of retries if pi not found immediately",
                        type=int, default=3)
    parser.add_argument('-v', help="verbosity",
                        action='count', default=0)

    args = parser.parse_args(argv[1:])
    if args.v > 1:
        logging.basicConfig(level=logging.DEBUG)
    elif args.v > 0:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    update_ssh_conf = args.update_ssh_config
    retries = args.retries

    if not update_ssh_conf:
        logger.info("`--update-ssh-config` not specified; will not create ssh.conf entries")

    pi_addrs = net.find_pis(retries)
    if not pi_addrs:
        raise ValueError("Raspberry PI not found!")

    print(
        "\nFound {} Pi's...\n"
        "{}".format(len(pi_addrs), "\n".join(map(str, pi_addrs)))
    )

    if update_ssh_conf:
        add_to_ssh_conf(pi_addrs)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
