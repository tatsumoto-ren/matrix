import httpx

from .server_info import ServerInfo, rm_port, version_trim


def joinmatrix_url():
    return 'https://joinmatrix.org/servers.json'


async def download_joinmatrix(client: httpx.AsyncClient) -> list[ServerInfo]:
    data: httpx.Response = await client.get(joinmatrix_url())
    data: list[dict] = data.json()
    out = []
    for server in data:
        out.append(ServerInfo(
            name=rm_port(server['name']),
            url=rm_port(server['domain']),
            country=server['jurisdiction'],
            open_signups=server['open'],
            software=server['software'],
            version=version_trim(server['version']),
        ))

    print(f"Joinmatrix nodes: {len(out)}")
    return out
