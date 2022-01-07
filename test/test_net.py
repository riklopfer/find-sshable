import json

from find_sshable import net


def test_get_network():
    network = net.get_network()
    assert network


def test_find_devices():
    devices = net.find_sshable(host_timeout="1ms")
    print(f"all ssh-able:\n{json.dumps(devices, indent=2)}")
    assert devices


def test_find_pi():
    pi_devices = net.find_hosts(host_timeout="1ms")
    print(f"pi devices: {pi_devices}")
    assert pi_devices is not None
