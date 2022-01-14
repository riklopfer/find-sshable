import sys

from find_sshable import command


def test_main():
    command.main(["main", "--host-pattern", ".*"])


def test_find_raspberrypi():
    command.main(["main", "--host-pattern", "raspberrypi"])


def test_main_no_args():
    sys.argv = ["main"]
    command.main_no_args()
