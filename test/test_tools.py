from find_raspi import net


def test_get_network():
    network = net.get_network()
    assert network


def test_find_devices():
    devices = net.find_sshable()
    assert devices


def test_find_pi():
    pi_addr = net.find_pis()
    print(pi_addr)
