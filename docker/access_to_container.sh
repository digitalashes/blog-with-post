#!/usr/bin/env bash

set -e

NAME="$1"
docker exec -it ${NAME} bash
