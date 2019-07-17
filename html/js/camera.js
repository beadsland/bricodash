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

var cooldown =  10 * 60

/*
  Grab responses until you can update feed with a good frame.
*/
async function fetch_frame(node, snap, hook, cool = null) {
  var opt =  { responseType: 'blob', timeout: 10000 };
  var response = await coolfetch(snap, opt, cooldown, cool);

  while (!response.ok) {
    response = await coolfetch(snap, opt, cooldown, response.cool);
    await sleep(100);
  }

  return response
}

/*
 Convert blob to frame.
 */
async function insert_blob(node, blob, oldObjectURL) {
  var newObjectURL = URL.createObjectURL(blob);
  node.src = newObjectURL;
  URL.revokeObjectURL(oldObjectURL);
  return newObjectURL
}

/*
 Load camera snapshot, calling slack webhook when down, and cycling until up again.
 */
async function update_frame(node, snap, hook, oldObjectURL) {
  var response = await fetch_frame(node, snap, hook);
  var blob = new Blob([response.data]);
  var toss = await greytoss(blob);
  if (!toss) {
    var newObjectURL = await insert_blob(node, blob, oldObjectURL);
  }

  if (response.cool) {
    throwhook( hook, device + " is wonky :'(" );
    while(response.cool) {
      response = await fetch_frame(node, snap, hook, response.cool);
      var blob = new Blob([response.data]);
      var toss = await greytoss(blob);
      if (!toss) {
        newObjectURL = insert_blob(node, blob, newObjectURL);
      }
    }
    throwhook( hook, device + " is steady again :)" );
  }

  return newObjectURL;
};

/*
  Pull frames of feed one at a time, rather than MJPEG.
 */
async function flipshow_loop(node, snap) {
  var oldObjectURL;
  var newObjectURL;

  var hook = await gethook(".keys/netops_hook")
  //throwhook( hook, device + " launching on dashcast reload =D" )

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
