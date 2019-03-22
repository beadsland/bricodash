#!/usr/bin/env python3

####
## Copyright © 2018 Beads Land-Trujillo.
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

# This will likely run as a systemd service in the long run, but
# for ease of development we'll do it as a cron job for now.
#
# This is an umbrella script that runs every minute and triggers
# each of the underlying pull services for the dashboard. Primarily,
# this is to limit cron clutter, but also, to avoid errors with
# cron syntax.
#
# crontab user: hm

import datetime
import os
import sys

min = datetime.datetime.now().minute
hr = datetime.datetime.now().hour
pwd = os.path.dirname(sys.argv[0])

if 1:                os.system(pwd + "/../jobs/weather.py &")
if 1:                os.system(pwd + "/../jobs/slack.py &")
if 1:                os.system(pwd + "/../jobs/mta.py &")
if min % 5 == 0:     os.system(pwd + "/../jobs/photo.py &")
if min % 60 == 0:    os.system(pwd + "/../jobs/wiki.py &")
if min % 10 == 0:    os.system(pwd + "/../jobs/events.py &")
if (hr+6) % 12 == 0: os.system(pwd + "/../jobs/thehaps.py &")
if 1:                os.system(pwd + "/../jobs/sous/veil.py &")

if 1:                os.system(pwd + "/../jobs/nap/upt.py &")
if min == 0 and hr % 6 == 0:
                     os.system(pwd + "/../jobs/nap/chk.py &")
