from find_sshable import command


def test_command():
    command.main(["main", "--host-pattern", ".*"])
