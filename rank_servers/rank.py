import functools
import json
import os
import re
from typing import Any, NewType, Dict, List, Tuple

import requests

try:
    from .consts import *
    from .synapse_version import SynapseVersion
except ImportError:
    from consts import *
    from synapse_version import SynapseVersion

Node = NewType('Node', Dict[str, Any])
rm_port = functools.partial(re.sub, r':\d+$', '', )


def fix_format(nodes: List[Node]) -> Dict[str, Node]:
    reformatted = {}
    for node in nodes:
        node['name'] = rm_port(node['name'])
        node['host'] = rm_port(node['host'])
        node['norm_version'] = SynapseVersion(node['version'])
        node['version'] = re.sub(r' \(.+\)$', '', node['version'])

        try:
            for key, value in reformatted[node['name']].items():
                reformatted[node['name']][key] = node[key] or value
        except KeyError:
            reformatted[node['name']] = node

    return reformatted


class SortServers:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self.min_synapse_ver = self.calc_min_ver()
        self.blocklist = self.construct_blocklist()

    @staticmethod
    def sorting_tuple(node: Node) -> Tuple[int, int, str]:
        return (
            node['norm_version'],
            -len(node['name']),
            node['name'],
        )

    @staticmethod
    def calc_min_ver() -> Tuple[int]:
        latest_ver = os.getenv('LATEST_SYNAPSE')
        assert latest_ver.startswith('1.')
        digits = [int(digit) for digit in latest_ver.split('.')]
        digits[1] -= 1
        digits[2] = 0
        return tuple(digits)

    @staticmethod
    def blocklist_escape(s: str) -> str:
        return s.replace('.', r'\.').replace('*', '.*')

    def construct_blocklist(self) -> List[str]:
        blocklist = []
        with open(os.path.join(DATA_DIR, 'blocklist.json')) as f:
            for server in json.load(f):
                blocklist.append(self.blocklist_escape(server['name']))
                if server['name'].startswith('*.'):
                    blocklist.append(self.blocklist_escape(server['name'][2:]))

        return blocklist

    def blocklisted(self, node_name: str) -> bool:
        for pattern in self.blocklist:
            if re.match(pattern, node_name):
                return True
        return False

    def filter_node(self, node: Node) -> bool:
        return all((
            node['version'].startswith('1.'),
            node['openSignups'] is True,
            node['norm_version'] >= self.min_synapse_ver,
            not self.blocklisted(node['name']),
        ))

    def run(self):
        nodes = sorted(
            filter(self.filter_node, self.nodes),
            key=self.sorting_tuple,
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
        if result.status_code != 200:
            raise RuntimeError("Failed to fetch server list.")
        with open(JSON_FILEPATH, 'w') as of:
            json.dump(json.loads(result.content), of, indent=4, ensure_ascii=False)
    with open(JSON_FILEPATH, 'r') as f:
        nodes = json.load(f)['data']['nodes']

    nodes = list(fix_format(nodes).values())

    SortServers(nodes).run()


if __name__ == '__main__':
    rank_servers()
