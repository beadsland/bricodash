#!/bin/bash

LCAP=5
while [ 1 == 1 ]; do
    LOAD=$(awk '{print $1}' /proc/loadavg)
    if [ $(bc -l <<< "$LOAD > $LCAP") -eq 1 ]; then
        echo Load too high, killing Chromium
        pkill chromium
    fi
    sleep 15
done
