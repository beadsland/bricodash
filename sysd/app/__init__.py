"""
Entry point for loop to run DashCast semi-persistently on a Chromecast while
allowing other Chromecast apps to work also by only launching when idle.

Based on https://github.com/madmod/dashcast-docker

Adapted for hackmanhattan/defaultcast by @mz@hackmanhattan.slack.com, 2017.
"""

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = True

import pychromecast
import time

import app.launch

def main(DISPLAY_NAME, DASHBOARD_URL, IGNORE_CEC):
    logger.debug('Hello defaultcast')

    if IGNORE_CEC:
        logger.debug('Ignoring CEC for Chromecast ' + DISPLAY_NAME)
        pychromecast.IGNORE_CEC.append(DISPLAY_NAME)

    casts = []
    attempt = 0

    while attempt < 5 and len(casts) == 0:
        logger.debug('Searching for Chromecasts...')
        casts = pychromecast.get_chromecasts()

        if len(casts) == 0 and attempt == 4:
            logger.debug('No Devices Found')
            exit()

        if len(casts) == 0:
            attempt += 1
            time.sleep(30)

    cast = (cc for cc in casts if DISPLAY_NAME in (None, '') \
                                  or cc.device.friendly_name == DISPLAY_NAME)
    cast = list(cast)

    if not len(cast):
        logger.debug('Chromecast with name ' + DISPLAY_NAME + ' not found')
        exit()
    else:
      cast = cast[0]

    defaultcast = app.launch.DashboardLauncher(cast, dashboard_url=DASHBOARD_URL)
    logger.info('Chromecast identified: %s' % defaultcast)

    try:
        while True:
            defaultcast.check()
    except Exception as e:
        logger.debug(e)
        exit()
