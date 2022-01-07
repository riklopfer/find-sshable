import os.path

from find_sshable import sshconf

_THIS_LOC = os.path.dirname(os.path.normpath(__file__))
_SAMPLE_PATH = os.path.join(_THIS_LOC, "sample_config.txt")


def test_load_config_parts():
    raspi, other = sshconf._load_config_parts(_SAMPLE_PATH)
    assert raspi
    assert other


def test_load_entries():
    entries = sshconf.get_raspi_hosts(_SAMPLE_PATH)
    assert entries


def test_update_entries():
    entries = sshconf.get_raspi_hosts(_SAMPLE_PATH)
    assert entries

    sshconf.update_raspi_hosts(entries, _SAMPLE_PATH, backup=False)
    entries_2 = sshconf.get_raspi_hosts(_SAMPLE_PATH)
    assert entries == entries_2

    backup_pth = _SAMPLE_PATH + ".bak"

    new_entries = [sshconf.HostEntry(name="fake", User="me", HostName="you")]
    sshconf.update_raspi_hosts(new_entries, _SAMPLE_PATH, backup=True)
    assert new_entries == sshconf.get_raspi_hosts(_SAMPLE_PATH)

    assert entries == sshconf.get_raspi_hosts(backup_pth)

    sshconf.update_raspi_hosts(entries, _SAMPLE_PATH)
    assert entries == sshconf.get_raspi_hosts(_SAMPLE_PATH)
