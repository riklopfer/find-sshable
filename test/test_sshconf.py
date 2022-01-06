import os.path

from find_raspi import sshconf

_THIS_LOC = os.path.dirname(os.path.normpath(__file__))
_SAMPLE = os.path.join(_THIS_LOC, "sample_config.txt")


def test_load_config_parts():
    raspi, other = sshconf._load_config_parts(_SAMPLE)
    assert raspi
    assert other
    print(raspi)


def test_load_entries():
    entries = sshconf.get_rapi_hosts(_SAMPLE)
    assert entries


def test_persist_entries():
    entries = sshconf.get_rapi_hosts(_SAMPLE)
    assert entries

    sshconf.update_rapi_hosts(entries, _SAMPLE)
    entries_2 = sshconf.get_rapi_hosts(_SAMPLE)
    assert entries == entries_2
