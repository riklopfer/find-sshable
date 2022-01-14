#!/usr/bin/env bash
set -e

usage() { 
echo "Usage: $0 [-h] [<install_dir>]
<install_dir> defaults to $HOME/bin
-h :: display this message" 2>&1
}

while getopts "h" Option; do
    case "${Option}" in
        h) 
            usage
            exit 0
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

# override INSTALL_LOC with first arg
INSTALL_LOC=$HOME/bin
if [[ $1 ]]; then
    INSTALL_LOC="$1"
fi

echo "Installing in $INSTALL_LOC"

mkdir -p $INSTALL_LOC

VENV_DIR=$INSTALL_LOC/.find-sshable 

if [[ ! -d $VENV_DIR ]]; then
    python3 -m venv $VENV_DIR
fi

$VENV_DIR/bin/pip install -U pip
$VENV_DIR/bin/pip install -U find-sshable

rm -f $INSTALL_LOC/find-sshable
ln -s $VENV_DIR/bin/find-sshable $INSTALL_LOC/find-sshable
