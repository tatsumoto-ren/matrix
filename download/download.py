#!/usr/bin/python3

import argparse
import asyncio
import dataclasses
import json
import sys
import traceback

import httpx

from .server_info import ServerInfo
from .sources.asra import download_asra
from .sources.joinmatrix import download_joinmatrix
from .sources.thefederation import download_thefederation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Downloader")
    parser.add_argument("-o", "--output", type=str, help="Output file.", required=True)
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    print("Output:", args.output)
    servers = {}
    async with httpx.AsyncClient(timeout=90) as client:
        tasks = [
            download_asra(client),
            download_joinmatrix(client),
            download_thefederation(client),
        ]
        for fut in asyncio.as_completed(tasks):
            try:
                result: list[ServerInfo] = await fut
            except httpx.HTTPStatusError as ex:
                traceback.print_exc(file=sys.stdout)
                continue
            servers |= {server.name: dataclasses.asdict(server) for server in result}

    with open(args.output, 'w') as of:
        json.dump(list(servers.values()), of, indent=4)
