import httpx

from ..server_info import ServerInfo, rm_port, version_trim


def joinmatrix_url():
    return 'https://servers.joinmatrix.org/servers.json'


async def download_joinmatrix(client: httpx.AsyncClient) -> list[ServerInfo]:
    data: httpx.Response = await client.get(joinmatrix_url())
    data: list[dict] = data.json()
    out = []
    for server in data['public_servers']:
        out.append(ServerInfo(
            name=rm_port(server['name']),
            url=rm_port(server['client_domain']),
            country=server['staff_jur'],
            open_signups=True,
            software=server['software'],
            version=version_trim(server['version']),
            sourced_from="Join Matrix",
        ))

    print(f"Joinmatrix nodes: {len(out)}")
    return out
