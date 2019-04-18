
"""
Launcher class to run DashCast semi-persistently on a Chromecast while
allowing other Chromecast apps to work also by only launching when idle.

Based on https://github.com/madmod/dashcast-docker

Adapted for hackmanhattan/defaultcast by @mz@hackmanhattan.slack.com, 2017.
"""

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = True

import time

import pychromecast.controllers.dashcast as dashcast

class DashboardLauncher():
    def __init__(self, device, dashboard_url='https://home-assistant.io', dashboard_app_name='DashCast'):
        self.device = device
        logger.debug('DashboardLauncher ' + self.device.name)

        self.controller = dashcast.DashCastController()
        self.device.register_handler(self.controller)

        receiver_controller = device.socket_client.receiver_controller
        receiver_controller.register_status_listener(self)

        self.dashboard_url = dashboard_url
        self.dashboard_app_name = dashboard_app_name

        self.launch_checked = 0

    def check(self):
        """ Called when a new cast status has been received."""
        self.launch_checked += 1
        logger.debug('Checking if we should launch. (i: {})'
                     .format(self.launch_checked))
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
        return ((self.device.status is not None and
                 self.device.status.display_name in ('Backdrop',)) or
                (self.launch_checked > 2880 and
                 time.localtime().tm_hour == 3 and
                 self.device.status is not None and
                 self.device.status.display_name in ('DashCast',)))

    def launch_dashboard(self):
        logger.debug('Launching dashboard on Chromecast ' + self.device.name)
        try:
            self.controller.load_url(self.dashboard_url)
            self.launch_checked = 0
        except Exception as e:
            logger.debug(e)
            pass
