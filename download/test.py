import asyncio
import sys

import httpx

from pathlib import Path


def set_package():
    global __package__

    if __name__ == '__main__' and __package__ is None:
        file = Path(__file__).resolve()
        parent, top = file.parent, file.parents[1]

        sys.path.append(str(top))
        sys.path.remove(str(parent))

        __package__ = 'download'


async def test():
    set_package()

    from .sources.asra import download_asra
    from .sources.joinmatrix import download_joinmatrix
    from .sources.thefederation import download_thefederation

    async with httpx.AsyncClient(timeout=90) as client:
        tasks = [
            download_asra(client),
            download_joinmatrix(client),
            download_thefederation(client),
        ]

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(test())
