def validate_timeout(time_str: str) -> str:
    units = time_str.lstrip("0123456789")
    if units.startswith('.'):
        units = units[1:]
    units = units.lstrip("0123456789")

    assert not units or units in ('h', 'm', 's', 'ms'), \
        f"Invalid time string {time_str}"
    return time_str
