#!/usr/bin/env bash

set -e

TIME_SLEEP="$1"
shift
cmd="$@"
sleep ${TIME_SLEEP}
exec ${cmd}
