#!/bin/bash -e

latest_synapse() {
	local -r synapse_pkgbuld='https://raw.githubusercontent.com/archlinux/svntogit-community/packages/matrix-synapse/trunk/PKGBUILD'
	curl -s "$synapse_pkgbuld" | grep -Po '(?<=pkgver=1\.)\d+'
}

# shellcheck disable=SC2155
{
	readonly this=$(readlink -f -- "$0")
	readonly dir=$(dirname -- "$this")
	readonly MATRIX_DATA_DIR=$dir/res
	readonly LATEST_SYNAPSE=$(latest_synapse)
}

mkdir -p -- "$MATRIX_DATA_DIR"
cd -- "$dir" || exit 1

echo "Latest synapse version: $LATEST_SYNAPSE"

export MATRIX_DATA_DIR LATEST_SYNAPSE

rm -- "$MATRIX_DATA_DIR/servers.json" || true
python3 -m rank_servers
mv -- "$MATRIX_DATA_DIR/formatted.html" "$dir/index.html"
mv -- "$MATRIX_DATA_DIR/result.tsv" "$dir/result.tsv"

echo "Done."
