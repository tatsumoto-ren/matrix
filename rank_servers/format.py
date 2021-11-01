import csv

try:
    from .consts import *
except ImportError:
    from consts import *


def format_entries():
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
                        f'<b>Version</b><code class="version">{row["version"]}</code>',
                        f'<b>Host</b><input class="host" readonly type="text" value="{row["host"]}">',
                        f'<b>Country</b><span class="country">{row["country"] or "Not specified"}</span>',
                        '</div>',
                        '</details>',
                        sep='\n',
                        file=of,
                    )


if __name__ == '__main__':
    format_entries()
