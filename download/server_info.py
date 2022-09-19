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
    sourced_from: str


def rm_port(url: str) -> str:
    return re.sub(r':\d+$', '', url)


def version_trim(version: str) -> str:
    return re.sub(r'\s*\(.+\)', '', version)
