#!/usr/bin/env python3 -u

"""
Run DashCast semi-persistently on a Chromecast while allowing other
Chromecast apps to work also by only launching when idle.

Based on https://github.com/madmod/dashcast-docker

Adapted for hackmanhattan/defaultcast by @mz@hackmanhattan.slack.com, 2017.

Revised for use with HDMI-CEC by @mz@hackmanhattan.slack.com, 2019.
"""

import os
import atexit
import sys
import time

def all_done():
  logger.info('all_done()')
  sys.stdout.flush()
  time.sleep(1)
atexit.register(all_done)

import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Hello")

import app  # import here to enforce logging

DASHBOARD_URL = os.getenv('DASHBOARD_URL', 'https://home-assistant.io')
DISPLAY_NAME = os.getenv('DISPLAY_NAME')
IGNORE_CEC = os.getenv('IGNORE_CEC') == 'True'

logger.info("%s %s" % (DISPLAY_NAME, IGNORE_CEC))
app.main(DISPLAY_NAME, IGNORE_CEC)
