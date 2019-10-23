#!/bin/bash
SCRIPT=$1
SCRIPT_ARG=$2
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
# echo $DIR

cd ~/python-pype-lang-2 && ./reinstall_from_source.sh
cd $DIR
python3 $SCRIPT $SCRIPT_ARG
