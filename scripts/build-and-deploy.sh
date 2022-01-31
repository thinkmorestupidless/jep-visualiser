#!/bin/sh

set -e -o pipefail -u

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR="$SCRIPT_DIR/.."

heroku login
heroku container:login
docker build --tag jep-visualiser "$ROOT_DIR"
heroku container:push web -a jep-visualiser
heroku container:release web -a jep-visualiser
