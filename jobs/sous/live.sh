#!/bin/sh

# www-data user must be in group with write access to pid/

cd `dirname $0`

touch pid/c$$

while [ 1 ]
do
  touch pid/l$$
  sleep 1
done
