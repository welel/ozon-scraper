#!/bin/sh

set -e

start_cron(){
  echo "start cron with jobs:"
  cat /cron/jobs
  touch /var/log/cron.log
  cron && tail -f /var/log/cron.log
}

start_cron

exit 0
