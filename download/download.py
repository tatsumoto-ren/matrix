#!/usr/bin/python3

import argparse
import asyncio
import dataclasses
import json

import httpx

from .sources.asra import download_asra
from .sources.joinmatrix import download_joinmatrix
from .sources.thefederation import download_thefederation


def parse_args():
    parser = argparse.ArgumentParser(prog="Downloader")
    parser.add_argument("-o", "--output", type=str, help="Output file.", required=True)
    return parser.parse_args()


async def main():
    args = parse_args()
    print("Output:", args.output)
    servers = {}
    async with httpx.AsyncClient(timeout=90) as client:
        tasks = [
            download_asra(client),
            download_joinmatrix(client),
            download_thefederation(client),
        ]
        for result in await asyncio.gather(*tasks):
            servers |= {server.name: dataclasses.asdict(server) for server in result}

    with open(args.output, 'w') as of:
        json.dump(list(servers.values()), of, indent=4)
