from find_sshable import net


def test_get_network():
    network = net.get_network()
    assert network


def test_find_sshable():
    sshable = net.find_sshable(host_timeout="1")
    print(f"ssh-able devices: {sshable}")
    assert sshable is not None


def test_do():
    res = net.is_sshable("192.168.86.20")
    assert res
    res = net.is_sshable("192.168.86.21")
    assert not res
    res = net.is_sshable("192.168.86.26")
    assert not res
