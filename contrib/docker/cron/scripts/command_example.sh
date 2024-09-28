#!/bin/sh

set -e

post_content(){
  echo "$(date) - post content..."
  export $(cat /proc/1/environ | tr '\0' '\n' | grep -v "^PATH=")
  /usr/local/bin/python3 /app/src/manage.py <command to run>
}

post_content

exit 0
