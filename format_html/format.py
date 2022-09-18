import csv
import json
import re

import argparse


def parse_args():
    parser = argparse.ArgumentParser(prog="Downloader")
    parser.add_argument("-o", "--output", type=str, help="Output file.", required=True)
    parser.add_argument("-i", "--input", type=str, help="Output file.", required=True)
    parser.add_argument("-b", "--blocklist", type=str, help="Path to blocklist.", required=True)
    parser.add_argument("-t", "--template", type=str, help="Path to template html.", required=True)
    return parser.parse_args()


def format_entries():
    args = parse_args()

    with open(args.blocklist) as bf:
        blocklist: list[dict[str, str]] = json.load(bf)
    with open(args.input) as rf, open(args.template) as tf, open(args.output, 'w') as of:
        reader = csv.DictReader(
            rf,
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
                        f'<b>Version</b><code class="version"><a target="_blank" href="https://federationtester.matrix.org/#{row["url"]}">{row["version"]}</a></code>',
                        f'<b>Host</b><input class="host" readonly type="text" value="{row["url"]}">',
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
