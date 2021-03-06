# bricodash

## Notices

This project draws together a number of resources from other creators,
used under various licenses. Please see [NOTICES.md](NOTICES.md) for
more details.

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

For more discussion, see:
[Hack Manhattan Wiki&mdash;Bricodash](https://wiki.hackmanhattan.com/Bricodash).

## Server Dependencies

* Apache2 + mods cgid and headers enabled
* systemd
* python3 + [requirements.txt](requirements.txt)
* Perl + Date::Manip
* ImageMagick
* Common Lisp
* [Elixir](https://elixir-lang.org/install.html)
* [BindSight](https://wiki.hackmanhattan.com/BindSight) (experimental)

### API Credentials

Most of the APIs used (see [NOTICES.md]) require some variation on tokens or
keys, which may, in turn, represent apps registered with the developer tools
for the respective API. These keys are stored as text files under `jobs/keys`
(not checked into the repository).

To get each script using an API begins by retrieving its key via the
`brico.common.get_token` function. Each `get_token()` invocation represents
a key, or token, string that needs to be obtained for the API in question and
stored in a file under `jobs\keys`.

Note that, given the way Meetup's API wizard works, we don't have a single
token string used across queries. Instead, each query either uses a token
string unique to it, or else doesn't require a token string at all.

## Kiosk Dependencies

Developed for use under Chromecast or a single-board computer running
Chromium. No guarantees as to how it will behave on other browsers.

If running chromium in kiosk mode on Raspbian, install `fonts-noto` and
`fonts-symbola` for better (but perhaps not complete) emoji support.

## Setting Up

* install under /opt/bricodash
* soft link to /opt/bricodash/html from within your /var/www/html hierarchy
* install /sysd/defaultcast.service as you would any systemd service
* set up a dedicated user to run sysd/cron.py
* store keys for various scripts under jobs/.keys
* set up a dedicated group "hmweb", including both your cron user and www-data
* create subdirs owned by said group allowing g+w permissions:
  - html/pull
  - html/thmb
  - jobs/nap/sid
  - jobs/sous/pid
* configure html/util/camera.php and camera.py to point to your local
camera MJPG camera devices, as appropriate
