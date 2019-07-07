/*
<!--
####
## Copyright © 2019 Beads Land-Trujillo.
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published
## by the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.
####
*/

'use strict';

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

var urlParams = new URLSearchParams(window.location.search);
var whoami = urlParams.get("whoami");
if (!whoami) { whoami = "unknown client"};
var device = `Door camera feed (${whoami})`;

/*
 Load camera snapshot, calling slack webhook when down and up again.
 */

async function update_frame(node, snap, hook, oldObjectURL) {
  var response = await fetch(snap);

  var debug = document.querySelector(".bottom-left")
  debug.textContent = "Hello"

  if (!response.ok) {
    debug.textContent = "Down :'("
    node.src = "";
    var msg = device +  " has gone offline :'("
    await fetch(hook, { method: 'POST', body: JSON.stringify( { text: msg } ) });

    while (!response.ok) { response = await fetch(snap); await sleep(1000); }

    msg = device + " is online again :)"
    await fetch(hook, { method: 'POST', body: JSON.stringify( { text: msg } ) });
  }

  var blob = await response.blob();
  var newObjectURL = URL.createObjectURL(blob);
  node.src = newObjectURL;
  URL.revokeObjectURL(oldObjectURL);

  return newObjectURL;
};

/*
  Pull frames of feed one at a time, rather than MJPEG.
 */

async function flipshow_loop(node, snap) {
  var hook_url = ".keys/netops_hook"
  var response = await fetch(hook_url)
  var hook = await response.text()

  var oldObjectURL;
  var newObjectURL;
  while(true) {
    newObjectURL = await update_frame(node, snap, hook, oldObjectURL);
    oldObjectURL = newObjectURL;
  }
};

function launch_doorcam() {
  var cam = document.querySelector("#door-cam");
  var snap = cam.src;
  snap = snap + "&action=snapshot"

  flipshow_loop(cam, snap);
}
