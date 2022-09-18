import re
import asyncio
import httpx


class SynapseVersion(tuple):
    @classmethod
    def from_str(cls, version_str: str):
        version_str = re.sub(r' \(.+\)$', '', version_str)
        version_digits = []
        for digit in version_str.split('.'):
            try:
                version_digits.append(int(re.match(r'\d+', digit).group()))
            except (ValueError, AttributeError):
                pass
        return cls(version_digits)


def synapse_pkgbuild_url() -> str:
    return 'https://raw.githubusercontent.com/archlinux/svntogit-community/packages/matrix-synapse/trunk/PKGBUILD'


async def fetch_latest_synapse_ver() -> SynapseVersion:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(synapse_pkgbuild_url())

    for line in response.text.splitlines():
        if 'pkgver=' in line:
            return SynapseVersion.from_str(line.split('=')[-1])


async def calc_min_synapse_ver() -> SynapseVersion:
    latest_ver: SynapseVersion = await fetch_latest_synapse_ver()
    assert latest_ver[0] == 1
    return SynapseVersion((1, latest_ver[1] - 1, 0,))


async def test():
    test_cases = [
        "0.25.1",
        "0.33.2.1",
        "0.33.3",
        "0.99.0",
        "0.99.1.1",
        "1.0.0",
        "1.1.0",
        "1.11.0",
        "1.11.1",
        "1.20.1",
        "1.2.1",
        "1.21.0",
        "1.30.1",
        "1.3.1",
        "1.31.0",
        "1.32.2",
        "1.35.1",
        "1.35.1 (b=master,c18d5837c,dirty)",
        "1.37.1",
        "1.37.1 (b=master,t=v1.37.1,c45246153)",
        "1.38.0",
        "1.39.0rc2",
        "1.4.0",
        "1.40.0",
        "1.4.1",
        "1.41.0",
        "1.41.0rc1",
        "1.41.1",
        "1.45.1",
        "1.45.1 (b=master,86a72d1)",
        "1.47.0rc2",
        "1.47.1",
        "1.47.1 (b=develop,7cebaf964)",
        "1.48.0",
        "1.48.0 (b=master,0ac04c7)",
        "1.49.0",
        "1.49.0 (b=master,61625d5)",
        "1.49.0 (b=master,a91698df9)",
        "1.49.0rc1",
        "1.49.0rc1 (b=develop,d6fb96e056)",
        "1.49.0rc1 (b=matrix-org-hotfixes,dbceb0068)",
        "1.49.2",
        "1.49.2 (b=aria-net)",
        "1.49.2 (b=master,9048bc8)",
        "1.49.2 (b=master,9ec46d623)",
        "1.49.2 (b=master,b2eb2d28)",
        "1.49.2 (b=rav/msc2775/server_side,05ea12a59)",
        "1.49.2 (b=release-v1.49,t=v1.49.2,6b6dcdc33)",
        "1.50.0a1",
        "1.5.1",
        "1.6.1",
        "1.7.3",
        "1.9.0",
        "1.9.1",
        "2.70.0",
        "3.11-for-workgroups",
        "1.66.0 (b=master,f0ebd13e,dirty)",
    ]

    for test_case in test_cases:
        print(SynapseVersion.from_str(test_case))

    min_ver = await calc_min_synapse_ver()
    print('min ver', min_ver)


if __name__ == '__main__':
    asyncio.run(test())
