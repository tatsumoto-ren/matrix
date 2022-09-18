#!/usr/bin/python3

import asyncio
import dataclasses
import json

import httpx

import argparse

from download.asra import download_asra
from download.joinmatrix import download_joinmatrix
from download.thefederation import download_thefederation


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
            download_joinmatrix(client),
            download_thefederation(client),
            download_asra(client),
        ]
        for result in asyncio.as_completed(tasks):
            servers |= {server.name: dataclasses.asdict(server) for server in await result}

    with open(args.output, 'w') as of:
        json.dump(list(servers.values()), of, indent=4)
