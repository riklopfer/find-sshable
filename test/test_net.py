from find_sshable import net


def test_get_network():
    network = net.get_network()
    assert network


def test_find_sshable():
    sshable = net.find_sshable(host_timeout="1")
    print(f"ssh-able devices: {sshable}")
    assert sshable is not None
