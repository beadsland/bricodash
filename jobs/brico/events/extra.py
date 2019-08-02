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

import brico.common
import brico.common.wiki

import re

def main():
  cal = []
  for l in brico.common.wiki.parse("Bricodash/Extra:Calendar").lists():
    for i in l.items:
      cols = i.lstrip().split("::")
      cols[0] = re.sub(r'[^A-Za-z0-9:\ +-,#]', '', cols[0])
      cal.append("::".join(cols))

  brico.common.write_text("extra.cal", cal)
