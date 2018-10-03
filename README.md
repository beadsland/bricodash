# bricodash

## Status

This project is a work-in-progress. Worse than that, it's a messy hack.

Scripts are structured only accidentally and barely procedural enough to
qualify as more than imperative, there's even less error checking than
documentation, and API queries throughout are no more sophisticated than
brute force.

In essence, the entire project is in desperate need of refactoring and
general cleanup. That's all next on the ToDo list,
along with some outstanding minor feature additions.

## Details

In October of 2017, Hack Manhattan installed a TV by the workspace tables.
To make it easily accessible to everyone in the space, we added a Chromecast.
To make that more useful, we're casting a "default" dashboard now. The same
default dashboard is also displayed on a screen over the intercom
at the entrance to our shop. This screen is driven by an old Raspberry Pi.

Bricodash represents a major revision to last year's defaultcast,
providing more functionality while using a thin-client architecture.

If the early version Raspberry Pi we're using is low powered, the Chromecast
is especially so. The goal has been to provide as much functionality as
possible while keeping client load to a minimum. With this in mind, we rely
heavily on server-side jobs to update various HTML components, allowing the
browser to poll for those files as needed.

**Dependencies:**

* Apache2 + mods cgid and headers enabled
* systemd
* python3 + [requirements.txt](requirements.txt)
* Perl + Date::Manip
* ImageMagick

Developed for use under Chromecast or a single-board computer running Chromium. No guarantees as to how it will behave on other browsers.

**Setting Up:**
* install under /opt/bricocast
* soft link to /opt/bricocast/html from within your /var/www/html hierarchy
* install /sysd/defaultcast.service as you would any systemd service
* set up a dedicated user to run sysd/cron.py
* store keys for various scripts under jobs/.keys
* set up a dedicated group including both your cron user and www-data
* create subdirs owned by said group allowing g+w permissions:
  - html/pull
  - html/thmb
  - jobs/nap/sid
  - jobs/sous/pid
* configure html/util/camera.php to point to your local camera MJPG camera devices, as appropriate
