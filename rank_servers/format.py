import csv
import json
import re

try:
    from .consts import *
except ImportError:
    from consts import *


def format_entries():
    with open(BLOCKLIST_FILEPATH) as bf:
        blocklist: list[dict[str, str]] = json.load(bf)
    with open(RESULT_FILEPATH) as rf, open(TEMPLATE_FILEPATH) as tf, open(FORMATTED_FILEPATH, 'w') as of:
        reader = csv.DictReader(
            rf,
            fieldnames=('name', 'version', 'host', 'country', 'flag'),
            dialect=csv.excel_tab
        )
        for line in tf:
            line = line.strip()
            if line:
                print(line, file=of)
            if line == '<!--formatted data begin-->':
                for row in reader:
                    print(
                        '<details class="entry">',
                        f'<summary>{row["name"]}</summary>',
                        '<div class="info">',
                        f'<b>URL</b><span class="name"><a target="_blank" href="https://{row["name"]}">{row["name"]}</a></span>',
                        f'<b>Version</b><code class="version"><a target="_blank" href="https://federationtester.matrix.org/#{row["host"]}">{row["version"]}</a></code>',
                        f'<b>Host</b><input class="host" readonly type="text" value="{row["host"]}">',
                        f'<b>Country</b><span class="country">{row["country"] or "Not specified"}</span>',
                        '</div>',
                        '</details>',
                        sep='\n',
                        file=of,
                    )
            if line == '<!--blocklist data begin-->':
                for row in blocklist:
                    name_pretty = re.sub(r"^\*\.", "", row["name"])
                    print(
                        '<details class="entry">',
                        f'<summary>{name_pretty}</summary>',
                        '<div class="info">',
                        f'<b>Host</b><input class="host" readonly type="text" value="{row["name"]}">',
                        f'<b>Reason</b><span class="reason">{row["reason"] or "Not specified"}</span>',
                        '</div>',
                        '</details>',
                        sep='\n',
                        file=of,
                    )


if __name__ == '__main__':
    format_entries()
