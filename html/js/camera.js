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

var cooldown =  5 * 60
var timeout = 1
var greycap = 20

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

var urlParams = new URLSearchParams(window.location.search);
var whoami = urlParams.get("whoami");
if (!whoami) { whoami = "unknown client"};
var device = `Door camera feed (${whoami})`;

/*
  Grab responses until you can update feed with a good frame.
*/
async function fetch_frame(node, snap, hook, cool = null) {
  var opt =  { responseType: 'blob', timeout: timeout * 1000 };
  var response = await coolfetch(snap, opt, cooldown, cool);

  while (!response.ok) {
    response = await coolfetch(snap, opt, cooldown, response.cool);
    await sleep(100);
  }

  return response
}

/*
 Convert blob to frame unless tossed.
 */
async function update_blob(node, snap, hook, toss = 0, cool = null) {
  var response = await fetch_frame(node, snap, hook, cool);
  var blob = new Blob([response.data]);
  var grey = await greytoss(blob);

  if (!grey) {
    var objectURL = URL.createObjectURL(blob);
    node.onload = function() { URL.revokeObjectURL(objectURL); }
    node.src = objectURL;
  } else {
    response['toss'] = toss + 1
    if (response.toss > greycap) {
      response['cool'] = new Date() / 1000 + cooldown
    }
  }

  return response
}

/*
 Load camera snapshot, calling slack webhook when down, and cycling until up again.
 */
async function update_frame(node, snap, hook, toss = 0) {
  var response = await update_blob(node, snap, hook, toss);

  if (response.cool) {
    if (response.toss) {
      throwhook( hook, device + " is wonky (corrupt frames) :'(" );
    } else {
      throwhook( hook, device + " is wonky (request timeout) :'(" );
    }
    while(response.cool) {
      response = await update_blob(node, snap, hook, response.toss, response.cool);
    }
    throwhook( hook, device + " is steady again :)" );
  }
  return response;
};
``
/*
  Pull frames of feed one at a time, rather than MJPEG.
 */
async function flipshow_loop(node, snap) {
  var hook = await gethook(".keys/netops_hook")
  throwhook( hook, device + " launching on Bricodash reload =D" )

  var response = {};
  while(true) {
    response = await update_frame(node, snap, hook, response.toss);
  }
};

function launch_doorcam() {
  var cam = document.querySelector("#door-cam");
  var snap = cam.src;
  snap = snap + "&action=snapshot"

  flipshow_loop(cam, snap);
}
