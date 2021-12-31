import requests

from . import rank, format

try:
    rank.rank_servers()
    format.format_entries()
except requests.ConnectionError:
    print("No internet?")
except RuntimeError as e:
    print(e)
