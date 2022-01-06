def test_get_network():
    network = tools.get_network()
    assert network


def test_find_devices():
    devices = tools.find_sshable()
    assert devices


def test_find_pi():
    pi_addr = tools.find_pis()
    print(pi_addr)
