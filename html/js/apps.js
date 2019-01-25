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
 Play slack notification when new message.
 */

function notifySlack() {
  var slack = document.querySelector("#slack-chat")
  forEach( slack.querySelectorAll(".slacked"), function(index, node) {
    var stamp = node.getAttribute("timestamp");
    if (slack.getAttribute("notifstamp") < stamp) {
      slack.setAttribute("notifstamp", stamp)
      if (slack.getAttribute("firstpass") === "done") {
        var audio = new Audio('snd/slack_sfx/knock_brush.mp3');
        audio.loop = false;
        audio.play();
      }
    }
  } )
  slack.setAttribute("firstpass", "done")
}

// https://toddmotto.com/ditch-the-array-foreach-call-nodelist-hack/
var forEach = function (array, callback, scope) {
  for (var i = 0; i < array.length; i++) {
    callback.call(scope, i, array[i]); // passes back stuff we need
  }
};

/*
 Alternate between building and space calendars.
 */

function buildingCal() {
  $("#upper_left_column").hide()
  $("#upper_left_column_alt").show()
  setTimeout(spaceCal, 1*60000)
}

function spaceCal() {
  $("#upper_left_column_alt").hide()
  $("#upper_left_column").show()
  setTimeout(buildingCal, 4*60000)
}

/*
 Show random photo
 */

function peekawait() {
  document.querySelector("#random_photo").style.zIndex = 0;
  setTimeout(peekaboo, 300000 + Math.random(600000));
}

function peekaboo() {
  document.querySelector("#random_photo").style.zIndex = 1000;
  $("#peekaboo").show(3000, peekabout);
}

function peekabout() { setTimeout(unpeekaboo, 2000); }

function unpeekaboo() { $('#peekaboo').hide(7000, peekawait); }

/*
 Position the H1
*/

function position_header() {
  console.log($(window).width())

  var h1 = "<h1>Welcome to Hack Manhattan!</h1>";
  if ($(window).width() < 1150) {
    document.querySelector("#inner_h1").innerHTML = "";
    document.querySelector("#outer_h1").innerHTML = h1;
  } else {
    document.querySelector("#outer_h1").innerHTML = "";
    document.querySelector("#inner_h1").innerHTML = h1;
  }
}

/*
 Reload camera feed if broken.
*/

function renewCam() {
  var cam = document.querySelector("#door-cam");
  var src = cam.src;
  src = src.replace(/#./, "")
  var dat = new Date()
  var mod = dat.getMinutes() % 2;
  cam.src = src + "#" + mod;
}
