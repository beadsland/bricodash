#!/usr/bin/env python3

"""
Run DashCast semi-persistently on a Chromecast while allowing other
Chromecast apps to work also by only launching when idle.

Based on https://github.com/madmod/dashcast-docker

Adapted for hackmanhattan/defaultcast by @mz@hackmanhattan.slack.com, 2017.
"""

import os
from daemonize import Daemonize

import app

DASHBOARD_URL = os.getenv('DASHBOARD_URL', 'https://home-assistant.io')
DISPLAY_NAME = os.getenv('DISPLAY_NAME')
IGNORE_CEC = os.getenv('IGNORE_CEC') == 'True'
DEBUG_FILE = os.getenv('DEBUG_FILE')

keep_fds = []
if DEBUG_FILE:
    fh = logging.FileHandler(DEBUG_FILE, "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    keep_fds.append(fh.stream.fileno())

app.main(DISPLAY_NAME, DASHBOARD_URL, IGNORE_CEC)

# We'll let systemd handle pid
#daemon = Daemonize(app="defaultcast", pid="/dev/null", action=main, keep_fds=keep_fds)
#daemon.start()
