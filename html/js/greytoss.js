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

function testgray(pixel) {
  if (pixel[3] == 0) return true;
  if (pixel[0] == 128 && pixel[1] == 128 && pixel[2] == 128) return true;
}

/*
  Inspect an image blob to determine if corrupt.
*/
async function greytoss(blob) {
  var objectURL = URL.createObjectURL(blob);
  var view = document.getElementById('door-cam');
  var img = new Image();
  img.src = objectURL;

  var count = 0 ;
  while (img.naturalWidth == 0 && count < 100) { await sleep(10); count = count + 1 }
  if (img.naturalWidth == 0) { return true; }

  var canvas = document.createElement('CANVAS');
  canvas.height = img.height;
  canvas.width = img.width;
  var context = canvas.getContext('2d');
  context.drawImage(img, 0, 0);
  URL.revokeObjectURL(objectURL)

  // reverse width & height when getting data
  var data = context.getImageData(img.width-1, img.height-1, 1, 1).data;
  if (testgray(data)) { return true; }
}
