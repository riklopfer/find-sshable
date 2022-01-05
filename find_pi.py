#!/usr/bin/env python3
import argparse
import logging
import os
import sys
from typing import Iterable

from find_pi import sshconf, tools

logger = logging.getLogger(os.path.basename(__file__))


def add_to_ssh_conf(addrs: Iterable[str], ssh_conf_prefix: str):
    if addrs is not None:
        addrs = list(addrs)

    assert addrs, "Addrs is empty"
    assert ssh_conf_prefix, "must provide ssh config prefix"

    if len(addrs) == 1:
        pi_names = [ssh_conf_prefix]
    else:
        pi_names = [ssh_conf_prefix]
        pi_names.extend(f"{ssh_conf_prefix}-{idx}"
                        for idx in range(1, len(addrs)))

    print(
        "Pi's will be added to your ssh config as follows\n"
        "{}".format("\n".join("\t".join(_)
                              for _ in zip(addrs, pi_names)))
    )

    # add it to your ssh config
    ssh_config_path = os.path.join(os.getenv("HOME", "/"), ".ssh", "config")
    if os.path.exists(ssh_config_path):
        with open(ssh_config_path) as ifp:
            config = sshconf.SshConfigFile(ifp)
    else:
        config = sshconf.empty_ssh_config_file()

    for addr, name in zip(addrs, pi_names):
        host = config.host(name)
        ssh_config_kwargs = dict(host=name, User="pi", HostName=addr)
        logger.info("Updated ssh Host entry for %s", name)

        if host:
            logger.warning("Overwriting ssh config entry: %s", host)
            config.set(**ssh_config_kwargs)
        else:
            config.add(**ssh_config_kwargs)

    config.write(ssh_config_path)


def main(argv):
    program_name = os.path.basename(argv[0])
    parser = argparse.ArgumentParser(prog=program_name)
    parser.add_argument('--ssh-prefix', '-p',
                        help="HostName for the raspberry pi will be added to your ssh.conf",
                        type=str)
    parser.add_argument('--retries', '-r',
                        help="Number of retries if pi not found immediately",
                        type=int, default=3)
    parser.add_argument('-v', action='count', default=0)

    args = parser.parse_args(argv[1:])
    if args.v > 1:
        logging.basicConfig(level=logging.DEBUG)
    elif args.v > 0:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    ssh_conf_prefix = args.ssh_prefix
    retries = args.retries

    pi_addrs = tools.find_pis(retries)
    pi_addrs = [str(_) for _ in pi_addrs]

    print(
        "Found {} Pi's...\n"
        "{}".format(len(pi_addrs), "\n".join(pi_addrs))
    )

    if ssh_conf_prefix:
        add_to_ssh_conf(pi_addrs, ssh_conf_prefix)
    else:
        logger.warning("`--ssh-prefix` not provided; will not create ssh.conf entries")


if __name__ == '__main__':
    sys.exit(main(sys.argv))
