#!/bin/bash

##
# Kill chromium when it gets greedy for memory.
#
# Provided by @mz@hackmanhattan.slack.com, 2019.
##

LCAP="4.8"

sleep 36000 # Wait for boot-cycle load to pass

while [ 1 == 1 ]; do
    LOAD=$(awk '{print $1}' /proc/loadavg)
    if [ $(bc -l <<< "$LOAD > $LCAP") -eq 1 ]; then
        echo Load too high, killing Chromium
        pkill chromium
    fi
    sleep 15
done
