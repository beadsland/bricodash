#!/usr/bin/env python3 -u

####
## Copyright © 2019 Beads Land-Trujillo.
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published
## by the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.
####

"""
Watch system load for trouble -- likely caused by Chrome getting carried away.
In event load gets excessive, reboot device to restore fresh system state.
"""

CAP = 8

import os
import multiprocessing
import time
import subprocess
import syslog

def adjusted_load():
  return os.getloadavg()[0] / multiprocessing.cpu_count()

syslog.syslog("Watchload daemon starting...")
while 1:
  time.sleep(1)
  if adjusted_load() > CAP:
    syslog.syslog("Watchload daemon rebooting system.")
    subprocess.call(['reboot'])
