#!/usr/bin/env bash
set -e

BIN_DIR=$HOME/bin
echo "Installing in $BIN_DIR"

mkdir -p $BIN_DIR

VENV_DIR=$BIN_DIR/.find-sshable 

if [[ ! -d $VENV_DIR ]]; then
    python3 -m venv $VENV_DIR
fi

$VENV_DIR/bin/pip install -U pip
$VENV_DIR/bin/pip install -U find-sshable

rm -f $BIN_DIR/find-sshable
ln -s $VENV_DIR/bin/find-sshable $BIN_DIR/find-sshable
