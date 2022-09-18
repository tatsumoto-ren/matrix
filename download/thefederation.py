import re

import httpx

from download.server_info import ServerInfo, rm_port


def thefederation_url():
    return 'https://the-federation.info/graphql?query=query%20Platform(%24name%3A%20String)%20%7B%0A%20%20platforms(name%3A%20%24name)%20%7B%0A%20%20%20%20name%0A%20%20%20%20code%0A%20%20%20%20displayName%0A%20%20%20%20description%0A%20%20%20%20tagline%0A%20%20%20%20website%0A%20%20%20%20icon%0A%20%20%20%20__typename%0A%20%20%7D%0A%20%20nodes(platform%3A%20%24name)%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%20%20version%0A%20%20%20%20openSignups%0A%20%20%20%20host%0A%20%20%20%20platform%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20icon%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20countryCode%0A%20%20%20%20countryFlag%0A%20%20%20%20countryName%0A%20%20%20%20services%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20__typename%0A%20%20%7D%0A%20%20statsGlobalToday(platform%3A%20%24name)%20%7B%0A%20%20%20%20usersTotal%0A%20%20%20%20usersHalfYear%0A%20%20%20%20usersMonthly%0A%20%20%20%20localPosts%0A%20%20%20%20localComments%0A%20%20%20%20__typename%0A%20%20%7D%0A%20%20statsNodes(platform%3A%20%24name)%20%7B%0A%20%20%20%20node%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20usersTotal%0A%20%20%20%20usersHalfYear%0A%20%20%20%20usersMonthly%0A%20%20%20%20localPosts%0A%20%20%20%20localComments%0A%20%20%20%20__typename%0A%20%20%7D%0A%7D%0A&operationName=Platform&variables=%7B%22name%22%3A%22matrix%7Csynapse%22%7D'


def get_software(server: dict):
    return server['platform']['name'].split('|')[-1].capitalize()


def fix_format(nodes: list[dict]) -> list[dict]:
    for node in nodes:
        node['name'] = rm_port(node['name'])
        node['host'] = rm_port(node['host'])
        node['version'] = re.sub(r'\s*\(.+\)', '', node['version'])
        node['software'] = get_software(node)
    return nodes


async def download_thefederation(client: httpx.AsyncClient) -> list[ServerInfo]:
    data: httpx.Response = await client.get(thefederation_url())
    data: dict = data.json()
    nodes = fix_format(data['data']['nodes'])
    out = []

    for server in nodes:
        out.append(ServerInfo(
            name=server['name'],
            url=server['host'],
            country=server['countryName'],
            open_signups=server['openSignups'],
            software=server['software'],
            version=server['version'],
        ))

    print(f"Thefederation nodes: {len(out)}")
    return out
