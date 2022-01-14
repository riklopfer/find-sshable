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

VENV_DIR=$INSTALL_LOC/.find-sshable 


rm -f $INSTALL_LOC/find-sshable
rm -rf $VENV_DIR
