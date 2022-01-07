import re

_VALID_SIMPLE_TIME = re.compile(r"\d+(:?\.\d+)?(?:h|m|s|ms)")


def simple_time_spec(time_str: str) -> str:
    """"""
    assert _VALID_SIMPLE_TIME.match(time_str), f"Invalid time string {time_str}"
    return time_str
