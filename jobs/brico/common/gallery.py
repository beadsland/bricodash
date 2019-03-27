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

import brico.common.html
import brico.common.thumb

thumb = brico.common.thumb.Cache()

###
# Thumbnail image gallery
###
class Line:
  def __init__(self, cap=5):
    self.images = []
    self.timestamp = None
    self.cap = cap

  def push(self, image, timestamp):
    if len(self.images) <= self.cap:
      self.images.append(image)
      if self.timestamp is None:
        self.timestamp = timestamp

  def str(self):
    line = [ thumb.get_thumb(i) for i in self.images ]
    line = [ brico.common.html.logo(i) for i in line ]

    return "…%s" % ''.join(line)
