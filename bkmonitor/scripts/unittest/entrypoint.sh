#!/bin/sh

set -e

/usr/sbin/mysqld --user=root &

redis-server &

exec "$@"
