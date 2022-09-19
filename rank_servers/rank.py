import argparse
import asyncio
import json
import re
import ssl

import httpx

from download.server_info import ServerInfo
from .synapse_version import SynapseVersion, calc_min_synapse_ver


def sorting_tuple(node: ServerInfo) -> tuple[SynapseVersion, int, str]:
    return (
        SynapseVersion.from_str(node.version),
        -len(node.name),
        node.name,
    )


class SortServers:
    def __init__(self, nodes: list[ServerInfo], blocklist: list[re.Pattern], min_synapse_ver: tuple[int]):
        self.nodes = nodes
        self.blocklist = blocklist
        self.min_synapse_ver = min_synapse_ver

        print(f"Min synapse version: {'.'.join(map(str, self.min_synapse_ver))}")

    def is_blocklisted(self, host: str) -> bool:
        for pattern in self.blocklist:
            if re.match(pattern, host):
                return True
        return False

    def filter_node(self, node: ServerInfo) -> bool:
        return (
                node.software.lower() == 'synapse'
                and node.version.startswith('1.')
                and node.open_signups is True
                and SynapseVersion.from_str(node.version) >= self.min_synapse_ver
                and not self.is_blocklisted(node.name)
                and not self.is_blocklisted(node.url)
        )

    def run(self) -> list[ServerInfo]:
        return sorted(
            filter(self.filter_node, self.nodes),
            key=sorting_tuple,
            reverse=True
        )


def parse_args():
    parser = argparse.ArgumentParser(prog="Rank servers")
    parser.add_argument("-o", "--output", type=str, help="Output file.", required=True)
    parser.add_argument("-i", "--input", type=str, help="Output file.", required=True)
    parser.add_argument("-b", "--blocklist", type=str, help="Path to blocklist.", required=True)
    return parser.parse_args()


def read_nodes(json_filepath: str):
    with open(json_filepath) as f:
        return list(map(lambda server: ServerInfo(**server), json.load(f)))


async def is_registration_open(client: httpx.AsyncClient, node: ServerInfo) -> bool:
    try:
        result = await client.post(
            f"https://{node.url}/_matrix/client/r0/register",
            json={"initial_device_display_name": "app.element.io (Mobile Safari, iOS)"}
        )
    except (httpx.HTTPError, ssl.SSLCertVerificationError):
        return False

    try:
        result_json = result.json()
    except json.decoder.JSONDecodeError:
        return False

    if "error" in result_json or "errcode" in result_json:
        return False

    for flow in result_json["flows"]:
        if "m.login.registration_token" in flow["stages"]:
            return False

    return True


async def filter_open(nodes: list[ServerInfo]) -> list[ServerInfo]:
    async with httpx.AsyncClient(timeout=10) as client:
        return [
            node
            for node, open_status
            in zip(nodes, await asyncio.gather(*(is_registration_open(client, node) for node in nodes)))
            if open_status is True
        ]


def blocklist_escape(s: str) -> re.Pattern:
    return re.compile(s.replace('.', r'\.').replace('*', '.*'), flags=re.IGNORECASE)


def construct_blocklist(blocklist_filepath: str) -> list[re.Pattern]:
    blocklist = []
    with open(blocklist_filepath) as f:
        for server in json.load(f):
            blocklist.append(blocklist_escape(server['name']))
            if server['name'].startswith('*.'):
                blocklist.append(blocklist_escape(server['name'][2:]))
    return blocklist


async def rank_servers():
    args = parse_args()
    blocklist = construct_blocklist(args.blocklist)

    nodes = read_nodes(args.input)
    min_synapse_ver = await calc_min_synapse_ver()
    nodes = SortServers(nodes, blocklist, min_synapse_ver).run()
    nodes = await filter_open(nodes)

    with open(args.output, 'w') as of:
        print("name", "version", "url", "country", sep='\t', file=of)
        for item in nodes:
            print(
                item.name,
                item.version,
                item.url,
                item.country,
                sep='\t',
                file=of
            )

    print(f"Total: {len(nodes)} nodes.")
