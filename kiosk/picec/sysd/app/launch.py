"""
Launcher class to run DashCast semi-persistently on a Chromecast while
allowing other Chromecast apps to work also by only launching when idle.

Based on https://github.com/madmod/dashcast-docker

Adapted for hackmanhattan/defaultcast by @mz@hackmanhattan.slack.com, 2017.

Revised for use with HDMI-CEC by @mz@hackmanhattan.slack.com, 2019.
"""

import logging
logger = logging.getLogger(__name__)

import time

class DashboardLauncher():
    def __init__(self, device, cec):
        self.device = device
        logger.debug('DashboardLauncher ' + self.device.name)
        self.cec = cec
        self.tv = cec.list_devices()[cec.CECDEVICE_TV]

    def check(self):
        """ Called when a new cast status has been received."""
        logger.debug('Checking if we should launch.')
        if self.device.status is not None:
            logger.debug('Current app: {}'
                         .format(repr(self.device.status.display_name)))

        if self.should_launch():
            logger.debug('I think we should launch. If this is the case in 15 seconds as well, we will launch.')
            time.sleep(15)

        # Launch also when we've been going for 12 hours continously and it's
        # 3am (no matter if a different app is active or it's our cast)
        if self.should_launch():
            self.launch_dashboard()

        time.sleep(15)

    def should_launch(self):
        """ If the device is active, the dashboard is not already active, and no other app is active."""
        return (self.tv.is_on() and self.device.status is not None and
                self.device.status.display_name in ('Backdrop',))

    def launch_dashboard(self):
        logger.debug('Launching dashboard')
        try:
            self.cec.set_active_source()
        except Exception as e:
            logger.debug(e)
            pass
