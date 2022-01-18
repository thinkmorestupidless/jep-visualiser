#!/bin/sh

set -e

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <port>"
  exit 1
fi

PORT=$1
BASE_DIR="/"
SCRIPT_DIR="/scripts"
SCRAPY_DIR="/scrapy"
WEBSITE_DIR="/www"

CONTAINER_ALREADY_STARTED="CONTAINER_STARTED"
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED
    echo "-- First container startup --"
    . "$SCRIPT_DIR/run.sh"
else
    echo "-- Not first container startup --"
fi