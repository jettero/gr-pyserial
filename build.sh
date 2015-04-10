#!/bin/bash

PREFIX="$1"
shift

if [ -z "$PREFIX" ]; then
    read -ep "PREFIX=" -i /usr/local PREFIX
fi

function remove_tmp() {
    rm -rvf /tmp/gr-pyserial.tmp-* \
        | grep --color=never directory:
}

tmp=$(mktemp -d /tmp/gr-pyserial.tmp-XXXXXXXXXX)
trap "remove_tmp; exit" 0 1 2 5 15

src_dir=$(dirname $(readlink -m $0))

if [ ! -n "$src_dir" -o ! -d "$src_dir" ]; then
    echo "couldn't figure out where $0 is"
    exit 1
fi

if [ -n "$tmp" -a -d "$tmp" ] && cd "$tmp"; then
    echo "created temp directory $tmp"

else
    echo error creating or using tmp directory
    exit 1
fi

set -e

cmake -Wno-dev "-DCMAKE_INSTALL_PREFIX=${PREFIX:-/usr/local}" "$src_dir"
make
sudo make install

if [ -n "$*" ]; then
    "$@"
fi
