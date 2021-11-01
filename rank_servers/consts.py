import json
import os

__all__ = [
    'URL',
    'JSON_FILEPATH',
    'RESULT_FILEPATH',
    'MIN_VERSION',
    'FORMATTED_FILEPATH',
    'TEMPLATE_FILEPATH',
    'BLOCKLIST'
]


def data_dir() -> str:
    if d := os.getenv('MATRIX_DATA_DIR'):
        return d
    elif os.path.isdir(d := os.path.join(os.pardir, 'res')):
        return d
    else:
        raise FileNotFoundError("Data dir not found.")


__d = data_dir()

URL = 'https://the-federation.info/graphql?query=query%20Platform(%24name%3A%20String)%20%7B%0A%20%20platforms(name%3A%20%24name)%20%7B%0A%20%20%20%20name%0A%20%20%20%20code%0A%20%20%20%20displayName%0A%20%20%20%20description%0A%20%20%20%20tagline%0A%20%20%20%20website%0A%20%20%20%20icon%0A%20%20%20%20__typename%0A%20%20%7D%0A%20%20nodes(platform%3A%20%24name)%20%7B%0A%20%20%20%20id%0A%20%20%20%20name%0A%20%20%20%20version%0A%20%20%20%20openSignups%0A%20%20%20%20host%0A%20%20%20%20platform%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20icon%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20countryCode%0A%20%20%20%20countryFlag%0A%20%20%20%20countryName%0A%20%20%20%20services%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20__typename%0A%20%20%7D%0A%20%20statsGlobalToday(platform%3A%20%24name)%20%7B%0A%20%20%20%20usersTotal%0A%20%20%20%20usersHalfYear%0A%20%20%20%20usersMonthly%0A%20%20%20%20localPosts%0A%20%20%20%20localComments%0A%20%20%20%20__typename%0A%20%20%7D%0A%20%20statsNodes(platform%3A%20%24name)%20%7B%0A%20%20%20%20node%20%7B%0A%20%20%20%20%20%20id%0A%20%20%20%20%20%20__typename%0A%20%20%20%20%7D%0A%20%20%20%20usersTotal%0A%20%20%20%20usersHalfYear%0A%20%20%20%20usersMonthly%0A%20%20%20%20localPosts%0A%20%20%20%20localComments%0A%20%20%20%20__typename%0A%20%20%7D%0A%7D%0A&operationName=Platform&variables=%7B%22name%22%3A%22matrix%7Csynapse%22%7D'
JSON_FILEPATH = os.path.join(__d, 'servers.json')
RESULT_FILEPATH = os.path.join(__d, 'result.tsv')
FORMATTED_FILEPATH = os.path.join(__d, 'formatted.html')
TEMPLATE_FILEPATH = os.path.join(__d, 'template.html')
try:
    MIN_VERSION = int(os.getenv('LATEST_SYNAPSE')) - 1
except TypeError:
    MIN_VERSION = 45
with open(os.path.join(__d, 'blocklist.json')) as f:
    BLOCKLIST = [server['name'] for server in json.load(f)]
