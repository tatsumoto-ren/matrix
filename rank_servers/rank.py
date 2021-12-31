import functools
import json
import os
import re
from typing import Any, NewType, Dict, List, Tuple

import requests

try:
    from .consts import *
except ImportError:
    from consts import *

Node = NewType('Node', Dict[str, Any])
rm_port = functools.partial(re.sub, r':\d+$', '', )


def blocklisted(node_name: str) -> bool:
    for pattern in BLOCKLIST:
        if re.match(pattern, node_name):
            return True
    return False


def filter_node(node: Node) -> bool:
    return all((
        node['version'].startswith('1.'),
        node['openSignups'] is True,
        node['norm_version'] >= MIN_VERSION,
        not blocklisted(node['name']),
    ))


def sorting_tuple(node: Node) -> Tuple[int, int, str]:
    return (
        node['norm_version'],
        -len(node['name']),
        node['name'],
    )


def fix_format(nodes: List[Node]) -> Dict[str, Node]:
    reformatted = {}
    for node in nodes:
        node['name'] = rm_port(node['name'])
        node['host'] = rm_port(node['host'])
        try:
            node['version'] = re.match(r'^\d+\.\d+\.[\d\w]*', node['version']).group()
            node['norm_version'] = float(re.match(r'^\d+\.(\d+)\.', node['version']).group(1))
        except AttributeError:
            node['norm_version'] = 0

        try:
            for key, value in reformatted[node['name']].items():
                reformatted[node['name']][key] = node[key] or value
        except KeyError:
            reformatted[node['name']] = node

    return reformatted


def sort_servers(nodes: List[Node]):
    nodes = sorted(
        filter(filter_node, nodes),
        key=lambda node: sorting_tuple(node),
        reverse=True
    )
    with open(RESULT_FILEPATH, 'w') as of:
        for item in nodes:
            print(
                item['name'],
                item['version'],
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
        nodes = json.load(f)['data']['nodes']

    nodes = list(fix_format(nodes).values())

    sort_servers(nodes)


if __name__ == '__main__':
    rank_servers()
