#!/bin/sh

set -u

SECRETS_PATH=${SECRETS_PATH:-/run/secrets}

log () {
  TIMESTAMP=$( date +%Y-%m-%d][%T.%3N )
  echo "[${TIMESTAMP}] ${*}"
}

for secret in "${SECRETS_PATH}"/*; do
  if [ -f "${secret}" ]; then
    log "[INFO] Found secret ${secret##*/}"
    export "${secret##*/}"="$(cat "$secret")"
  fi
done

env | cat - /crontab > /etc/crontabs/root

crond -L /var/log/cron/cron.log "$@" && tail -f /var/log/cron/cron.log

