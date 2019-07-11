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
  Wrapper for axios get to give us cleaner, fetch-like response as result.
*/

async function fetchlike(url, opt) {
  try {
    var response = await axios.get(url, opt);
    response['ok'] = true;
    return response;
  } catch (error) {
    if (error.response) {
      error.response['ok'] = false;
      return error.response;
    } else {
      return { ok: false }
    }
  }
}

/*
  Wrapper to track cooldown on bad requests.
  */

async function coolfetch(snap, opt, cool = null) {
  var response = await fetchlike(snap, opt);
  if (!response.ok) {
    response['cool'] = new Date() / 1000 + (10 * 60);
  } else {
    if (cool > new Date() / 1000) {
      response['cool'] = cool
    }
  }
  return response
}

/*
  Grab responses until you can update feed with a good frame.
  */

async function fetch_frame(node, snap, hook, cool = null) {
  var opt =  { responseType: 'blob', timeout: 10000 };
  var response = await coolfetch(snap, opt, cool);

  if (!response.ok) {
    while (!response.ok) {
      response = await coolfetch(snap, opt, response.cool);
      await sleep(100);
    }
  }

  return response
}

/*
 Convert blob to frame.
 */
function insert_blob(node, response, oldObjectURL) {
  var blob = new Blob([response.data]);
  var newObjectURL = URL.createObjectURL(blob);
  node.src = newObjectURL;
  URL.revokeObjectURL(oldObjectURL);
  return newObjectURL
}

/*
 Load camera snapshot, calling slack webhook when down and up again.
 */

async function update_frame(node, snap, hook, oldObjectURL) {
  var response = await fetch_frame(node, snap, hook);
  var newObjectURL = insert_blob(node, response, oldObjectURL);

  if (response.cool) {
    var msg = device + " is wonky :'("
    await fetch(hook, { method: 'POST', body: JSON.stringify( { text: msg } ) });
    console.log(msg)

    while(response.cool) {
      response = await fetch_frame(node, snap, hook, response.cool);
      newObjectURL = insert_blob(node, response, newObjectURL);
    }

    msg = device + " is steady again :)"
    await fetch(hook, { method: 'POST', body: JSON.stringify( { text: msg } ) });
    console.log(msg)
  }

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
