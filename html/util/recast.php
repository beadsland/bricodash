<!-- Stop the chromecast, allowing our systemd service to restart it fresh. -->

<!-- We are having issues with the camera stalling and/or the chromecast
     going black. The former seems to correct itself on its own after
     a time. Thinking perhaps a reboot will prevent the issue from
     arising, but need it to be under the control of the dashboard, not
     initiated when someone might be watching a video or whatnot. -->

<?php exec("export LC_ALL=C.UTF-8; export LANG=C.UTF-8; /usr/local/bin/catt stop");?>

<!-- Of course, this is open to DOS attacks, so really ought to figure out
     a way to determine dashcast uptime from the server-side rather than
     rely on the client to tell us when it needs a nap. -->
