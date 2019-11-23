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

window.onload = function() {
  launch_tabgc()
}

async function sleep(milliseconds) {
  var prom = new Promise(resolve => setTimeout(resolve, milliseconds))
  var resp = await prom
  return resp
}

async function launch_tabgc() {
  var urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has("gc_hours")) {
    var gc_hours = urlParams.get("gc_hours")
  } else {
    var gc_hours = 12
  }

  var url = window.location.pathname
  var filename = url.substring(url.lastIndexOf('/')+1);

  var dash = window.location.href
  dash = dash.replace(filename, "")

  while(1) {
    /* requires: --disable-popup-blocking switch in chrome */
    var newWin = window.open(dash, "_blank", function(win) {
      win.onload(function() { win.enterKioskMode() })
    })

    /* "fullscreen=yes,titlebar=no,resizeable=no") */


    await sleep(gc_hours * 60 * 60 * 1000)
    newWin.close()
  }
}
