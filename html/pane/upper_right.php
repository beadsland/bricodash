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
-->

<div class="container"
     style="background-size: contain; background-image: url('img/ceilingcat.jpg');">

  <!-- doorcam: 640 x 480 -->
  <img id="door-cam" src="util/camera.py?view=door">

  <div class="top-right"><?php include "weather.html"?></div>
  <div class="bottom-right">
    <span style="display: none;" id="testpass">0</span>
    <span style="display: none;" id="testing"><?php include "pane/tick.bool"?></span>
    <span id="clock"></span>
  </div>
  <div class="bottom-left"><span id="diagnostics" style="color: red;"></span></div>
</div>
