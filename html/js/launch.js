/*
<!--
####
## Copyright © 2018 Beads Land-Trujillo.
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

/*
 Start polling for back-end content.
 */
window.onload = function() {
  position_header();
  sousveil()

  setInterval(renewCam, 60000);
  setInterval(updateTime, 500);
  launch_weather();

  scheduleDiv("#wiki-edits", "pull/wiki.html", 30 * 60 * 1000);
  scheduleDiv("#mta-widget", "pull/mta.html", 45 * 1000);
  scheduleDiv("#slack-chat", "pull/slack.html", 30 * 1000);

  scheduleDiv("#space-events", "pull/space_events.html", 10 * 60 * 1000);
  scheduleDiv("#building-events", "pull/building_events.html", 10 * 60 * 1000);
  buildingCal()

  scheduleDiv("#random_photo", "pull/photo.html", 10 * 60 * 1000);
  peekawait();
}


/*
 Load a text file from server.
*/

function scheduleDiv(divID, pullPath, interval) {
  document.querySelector(divID).addEventListener('error', fixImage, true);
  updateDiv(divID, pullPath, interval);
  setInterval(function() { updateDiv(divID, pullPath, interval); }, interval);
}

/* Chrome disregards padding-left if inline image errors out rather than load.
   When image is within a hanging-indented span, the broken image icon is
   displaced to the left of where it is supposed to be. We fix this by
   giving the IMG tag a valid image to display, thereby forcing Chrome
   to again pay attention to padding-left. */
function fixImage(event) {
  if( event.target.tagName == 'IMG') { event.target.src = "img/broken.png"; }
}

function updateDiv(divID, pullPath, interval) {
  var xhttp = new XMLHttpRequest();
  xhttp.responseType = "text";
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200 && xhttp.response.length > 0) {
      var div = document.querySelector(divID);
      div.innerHTML = xhttp.response;
    };
    checkStale(divID, interval);
  }
  xhttp.open("GET", pullPath, true);
  xhttp.send();
}

/*
 Test if pull data is stale since last successful poll.
 */

function checkStale(divID, interval) {
  var mydiv = document.querySelector(divID);
  var e
  try {
    e = mydiv.querySelector("#timestamp").getAttribute("epoch");
  } catch (err) {
    e = 0;
  }

  var elapsed = new Date() / 1000 - e;

  if (elapsed > (interval / 1000 * 2)) {
    var err = document.createElement("div");
    err.className = "centered";
    var ico = document.createElement("span");
    ico.className = "timeout-error";
    err.appendChild(ico);
    mydiv.appendChild(err);
  }
}
