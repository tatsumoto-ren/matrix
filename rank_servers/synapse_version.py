import re


class SynapseVersion(tuple):
    def __new__(cls, version_str: str):
        version_str = re.sub(r' \(.+\)$', '', version_str)
        version_digits = []
        for digit in version_str.split('.'):
            try:
                version_digits.append(int(re.match(r'\d+', digit).group()))
            except (ValueError, AttributeError):
                pass

        return super().__new__(cls, version_digits)


def test():
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
    ]

    for test_case in test_cases:
        print(SynapseVersion(test_case))


if __name__ == '__main__':
    test()
