#!/bin/bash

LCAP=5
CPUS=$(cat /proc/cpuinfo | grep processor | wc -l)
while [ 1 == 1 ]; do
    LOAD=$(awk '{print $1}' /proc/loadavg)
    if [ $(bc -l <<< "$LOAD / $CPUS > $LCAP") -eq 1 ]; then
        pkill chromium
    fi
    sleep 15
done
