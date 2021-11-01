#!/usr/bin/python3

import json
import os
import re
from typing import Any, NewType

import requests

try:
    from .consts import *
except ImportError:
    from consts import *

Node = NewType('Node', dict[str, Any])


def filter_node(node: Node) -> bool:
    return all((
        node['version'].startswith('1.'),
        node['openSignups'] is True,
        node['norm_version'] >= MIN_VERSION,
        node['name'] not in BLOCKLIST,
    ))


def sorting_tuple(node: Node) -> tuple[int, int]:
    return (
        -node['norm_version'],
        len(node['name']),
    )


def fix_format(nodes):
    for node in nodes:
        node['name'] = re.sub(r':\d+$', '', node['name'])
        try:
            node['norm_version'] = float(re.match(r"^\d+\.(\d+)\.", node['version']).group(1))
        except AttributeError:
            node['norm_version'] = 0


def sort_servers(nodes: list[Node]):
    fix_format(nodes)
    nodes = sorted(
        filter(filter_node, nodes),
        key=lambda node: sorting_tuple(node),
    )
    with open(RESULT_FILEPATH, 'w') as of:
        for item in nodes:
            print(
                item['name'],
                re.match(r'\d+\.\d+\.[\d\w]*', item['version']).group(),
                item['host'],
                item['countryName'],
                item['countryFlag'],
                sep='\t',
                file=of
            )

    print(f"Total: {len(nodes)} nodes.")


def rank_servers():
    if not os.path.isfile(JSON_FILEPATH):
        with requests.Session() as s:
            result = s.get(URL)
        with open(JSON_FILEPATH, 'w') as of:
            json.dump(json.loads(result.content), of, indent=4)
    with open(JSON_FILEPATH, 'r') as f:
        nodes: list[Node] = json.load(f)['data']['nodes']

    sort_servers(nodes)


if __name__ == '__main__':
    rank_servers()
