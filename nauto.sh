#!/bin/bash

function usage {
    echo "usage: ${0} [-h help] [-c clean] [-m make]"
    echo "  -h      display this usage menu"
    echo "  -c      clean the cached files and temporary files"
    echo "  -m      make folder structure & download geckodriver executable"
}

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
        usage && exit 0
    ;;
    -c|--clean)
        rm -r "${DIR}"/project/server/tasks/ina/resources
        find "${DIR}"/project/server/tasks/ -type f -name "*.csv" -exec rm -r {} +
        find "${DIR}"/project/server/ -type d -name "__pycache__" -exec rm -r {} +
        find "${DIR}"/ -type f -name "*.log" -exec rm -r {} +
        exit 0
    ;;
    -m|--make)
        python3 "${DIR}/setup.py"
        exit 0
    ;;
    *)
    POSITIONAL+=("$1")
    shift
    ;;
esac
done
set -- "${POSITIONAL[@]}"
usage && exit 1