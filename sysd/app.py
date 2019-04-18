#!/usr/bin/env python3

"""
Run DashCast semi-persistently on a Chromecast while allowing other
Chromecast apps to work also by only launching when idle.

Based on https://github.com/madmod/dashcast-docker

Adapted for hackmanhattan/defaultcast by @mz@hackmanhattan.slack.com, 2017.
"""

import os
import daemonize
import sys

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

DASHBOARD_URL = os.getenv('DASHBOARD_URL', 'https://home-assistant.io')
DISPLAY_NAME = os.getenv('DISPLAY_NAME')
IGNORE_CEC = os.getenv('IGNORE_CEC') == 'True'
DEBUG_FILE = os.getenv('DEBUG_FILE')

keep_fds = []
if DEBUG_FILE:
    fh = logging.FileHandler(DEBUG_FILE, "w")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.info("Hello")
    keep_fds.append(fh.stream.fileno())

import app  # import here to enforce logging

import sys
sys.stdout = open(DEBUG_FILE, 'w')
print('test')

def daemon():
  app.main(DISPLAY_NAME, DASHBOARD_URL, IGNORE_CEC)

if len(sys.argv) > 1:
  daemon()
else:
  # We'll let systemd handle pid
  daemon = daemonize.Daemonize(app="defaultcast", pid="/dev/null",
                               action=daemon, keep_fds=keep_fds)
  daemon.start()
