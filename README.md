# defaultcast

In October of 2017, Hack Manhattan installed a TV by the workspace tables. To
make it easily accessible to everyone in the space, we added a Chromecast. To
make that more useful, we're casting a "default" dashboard now.

The same default dashboard is also displayed on a screen over the intercom
at the entrance to our shop. This screen is driven by a Raspberry Pi.

Based on [dashcast-docker](https://github.com/madmod/dashcast-docker)

Requires:

* [pychromecast](https://github.com/balloob/pychromecast) `876ed6c` and above
* daemonize
* systemd unless you want to write your own init scripts
* a variety of python and perl libraries
* apache 2 (for support of continuously running php scripts)

TODO:

* Still adding a variety of minor features.
* Source files are in desperate need of refactoring
* Probably ought to write a dependency install script
