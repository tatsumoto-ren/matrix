#!/bin/bash -e

readonly this=$(readlink -f -- "$0")
readonly dir=$(dirname -- "$this")
readonly MATRIX_DATA_DIR=$dir/res

mkdir -p -- "$MATRIX_DATA_DIR"
cd -- "$dir" || exit 1

export MATRIX_DATA_DIR
python3 -m rank_servers
mv -- "$MATRIX_DATA_DIR/formatted.html" "$dir/index.html"
echo "Done."
