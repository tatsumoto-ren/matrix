import httpx
import lxml.html

from ..server_info import ServerInfo, rm_port, version_trim


def asra_url():
    return 'https://wiki.asra.gr/en:public_servers'


async def download_asra(client: httpx.AsyncClient) -> list[ServerInfo]:
    data: httpx.Response = await client.get(asra_url())
    html: lxml.html.HtmlElement = lxml.html.fromstring(data.content)
    rows: list = html.xpath("//div[@class='sortable']//table//tr")
    out = []

    for tr in rows:
        tr: lxml.html.HtmlElement
        try:
            name, server, software, version, *_ = map(lxml.html.HtmlElement.text_content, tr)
            out.append(ServerInfo(
                name=rm_port(name),
                url=rm_port(server),
                country="Unknown",
                open_signups=True,
                software=software,
                version=version_trim(version),
                sourced_from="Asra.gr",
            ))
        except ValueError:
            pass

    print(f"Asra nodes: {len(out)}")
    return out
