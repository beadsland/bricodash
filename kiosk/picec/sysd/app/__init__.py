"""
Entry point for loop to run DashCast semi-persistently on a Chromecast while
allowing other Chromecast apps to work also by only launching when idle.

Based on https://github.com/madmod/dashcast-docker

Adapted for hackmanhattan/defaultcast by @mz@hackmanhattan.slack.com, 2017.

Revised for use with HDMI-CEC by @mz@hackmanhattan.slack.com, 2019.
"""

import logging
logger = logging.getLogger(__name__)

import pychromecast
import cec
import time

import app.launch

def main(DISPLAY_NAME, IGNORE_CEC):
    logger.debug('Hello defaultcast')
    cec.init()

    if IGNORE_CEC:
        logger.debug('Ignoring CEC for Chromecast %s', DISPLAY_NAME)
        pychromecast.IGNORE_CEC.append(DISPLAY_NAME)

    casts = []
    attempt = 0

    while attempt < 5 and not casts:
        logger.debug('Searching for Chromecasts...')
        casts = pychromecast.get_chromecasts()

        if not casts and attempt == 4:
            logger.debug('No Devices Found')
            exit()

        if not casts:
            attempt += 1
            time.sleep(30)

    cast = [cc for cc in casts if DISPLAY_NAME in (None, '') \
                                  or cc.device.friendly_name == DISPLAY_NAME]
    if not cast:
        logger.debug('Chromecast with name %s not found', DISPLAY_NAME)
        exit()
    else:
        cast = cast[0]

    defaultcast = app.launch.DashboardLauncher(cast, cec)
    logger.info('Chromecast identified: %s', defaultcast)

    try:
        while True:
            defaultcast.check()
    except Exception as err:
        logger.debug(err)
        exit()
