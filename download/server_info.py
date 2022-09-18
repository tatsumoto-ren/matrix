import dataclasses
import re


@dataclasses.dataclass(frozen=True)
class ServerInfo:
    name: str
    url: str
    country: str
    open_signups: bool
    software: str
    version: str


def rm_port(url: str):
    return re.sub(r':\d+$', '', url)
