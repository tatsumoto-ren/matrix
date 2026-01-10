#!/bin/bash

set -euo pipefail

readonly this=$(readlink -f -- "$0")
readonly dir=$(dirname -- "$this")

cd -- "$dir" || exit 1

mkdir -p temp

if ! [[ -d .venv ]]; then
	python -m venv .venv
	source .venv/bin/activate
	python -m pip install --upgrade -r requirements.txt
fi

if [[ $* == *debug ]]; then
	true
else
	python3 -m download --output "temp/all.json"
fi

python3 -m rank_servers --input "temp/all.json" --output "result.tsv" --blocklist "res/blocklist.json"
python3 -m format_html --input "result.tsv" --output "index.html" --template "res/template.html" --blocklist "res/blocklist.json"

echo "Done."
