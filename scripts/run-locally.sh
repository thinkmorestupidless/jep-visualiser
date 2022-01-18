#!/bin/sh

set -e -o pipefail -u

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
BASE_DIR="$SCRIPT_DIR/.."
SCRAPY_DIR="$BASE_DIR/scrapy"
WEBSITE_DIR="$BASE_DIR/www"
DATA_DIR="$WEBSITE_DIR/data"

## ensure dependencies are available

cd "$BASE_DIR"

if [ ! -d "$BASE_DIR/.venv" ]; then
    echo "create venv and install python dependencies"
    virtualenv .venv
fi

source .venv/bin/activate

if [ ! command -v scrapy &> /dev/null ]; then
cd "$SCRAPY_DIR"
    pip install -r requirements.txt
fi

# run the process

. "$SCRIPT_DIR/run.sh"