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

import brico.events.holiday
import brico.common.html

from collections import defaultdict
import re

def main():
  cal = brico.events.holiday.parse_cal("cal/birth.list")

  d = defaultdict(list)
  for x in cal:
    d[x[0]].insert( 0, re.compile(" ").sub("&nbsp;", x[1]) )
  d = {k: stringify(d[k]) for k in d.keys()}

  str = ""
  for dt in d.keys():
    str += "%s :: %s\n" % (dt.decode('utf-8'), d[dt])
  f = open("cal/birth.out", "w")
  f.write(str)
  f.close()

def stringify(names):
  cake = "birthday %s" % brico.common.html.emoji("🎂")
  if len(names) == 1:
    s = "%s's %s" % (names[0], cake)
  else:
    s = "'s, ".join(names)
    s = "%s's %s" % (s, cake)

  s = re.compile("s's").sub("s'", s)
  s = re.compile("\)'s").sub("", s)
  s = re.compile(r", ([^,]*)$").sub(r" & \1", s)
  return s
