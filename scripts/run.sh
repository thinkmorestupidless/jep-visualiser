#!/bin/sh

set -e

if [[ -z "$BASE_DIR" || -z "$SCRAPY_DIR" || -z "$SCRIPT_DIR" || -z "$WEBSITE_DIR" ]]; then
    echo "-- BASE_DIR, SCRAPY_DIR, SCRIPT_DIR and/or WEBSITE_DIR vars not set"
    echo "-- Are you running $(basename $0) directly? If so, try running via run-locally.sh" 
fi

DEFAULT_PORT=8000
WWW_PORT=${PORT:-$DEFAULT_PORT}

# create data directory

DATA_DIR="$WEBSITE_DIR/data"

if [ ! -d "$DATA_DIR" ]; then 
    mkdir "$DATA_DIR"
fi

# collect data

cd "$SCRAPY_DIR"
scrapy crawl jdk -O "$DATA_DIR/scraped-jdks.json"
scrapy crawl jep -O "$DATA_DIR/scraped-jeps.json"

# transform data

cd "$SCRIPT_DIR"
./create_timeline_data.py "$DATA_DIR" "$DATA_DIR"

# serve data

cd "$WEBSITE_DIR" 
python3 -m http.server "$WWW_PORT"
