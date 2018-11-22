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
 Sous veil ance
 */
 function sousveil() {
   var urlParams = new URLSearchParams(window.location.search);
   if (urlParams.has("whoami") && urlParams.get("whoami") === "chromecast") {
     scheduleDiv("#sous", "pull/sous.html", 1000);
     setInterval(eyeball, 500)
   }
 }

function eyeball() {
  var veil = document.querySelector("#veil");
  var eye = document.querySelector("#eye");
  var vop = veil.getAttribute("value");
  var eop = eye.style.opacity;
  if (vop === localStorage.eye_opacity) {
    if (eop > 0) {
      eye.style.opacity = eop * .9;
    }
  } else {
    eye.style.opacity = vop;
  }
  localStorage.eye_opacity = vop;
}
