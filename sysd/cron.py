#!/usr/bin/env python3

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
pwd = os.path.dirname(sys.argv[0])

if 1:                os.system(pwd + "/../jobs/slack.py")
if min % 10 == 0:    os.system(pwd + "/../jobs/meetup.py")
