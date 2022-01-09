import json

from find_sshable import net


def test_get_network():
    network = net.get_network()
    assert network


def test_find_devices():
    devices = net._scan_open_22(host_timeout="1")
    print(f"all ssh-able:\n{json.dumps(devices, indent=2)}")
    assert devices


def test_find_pi():
    pi_devices = net.find_sshable(host_timeout="1")
    print(f"pi devices: {pi_devices}")
    assert pi_devices is not None


def test_do():
    res = net.is_sshable("192.168.86.20")
    assert res
    res = net.is_sshable("192.168.86.21")
    assert not res
    res = net.is_sshable("192.168.86.26")
    assert not res
