#!/usr/bin/env python3

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

import os
import time
import sys

pwd = os.path.dirname(sys.argv[0])
pid = os.path.join(pwd, "pid")

ival = 60 * 2;

for i in range(1, ival):
  list = [ f for f in os.listdir(pid) if f.startswith("l") ]
  list = [ (os.path.join(pid, f.replace("l", "c")), os.path.join(pid, f)) for f in list ]
  list = [ t for t in list if os.path.isfile(t[0]) ]
  list = [ (os.path.getmtime(t[0]), os.path.getmtime(t[1])) for t in list ]
  list = [ (t[1]-t[0], time.time()-t[1]) for t in list ]

  result = []
  for t in list:
    live = 60 / ( t[0] + .0001 )
    if t[1] < 1.1:
      result.append( live )
    else:
      dead = 2 / ( t[1] + .0001 )
      result.append( min([dead, dead * live, live]) )

  result = str(sum(result))
  result = '<span id="veil" value="' + result + '"></span>'
  result += '<span id="timestamp" epoch="' + str(time.time() + 2) + '"></span>'

  filename = os.path.join(pwd, "../../html/pull/sous.html")

  file = open(filename + ".new", "w")
  file.write( result )
  file.close()
  os.rename(filename + ".new", filename)

  time.sleep(60 / ival)

#  time.sleep(5)

for f in os.listdir(pid):
  f = os.path.join(pid, f)
  if os.stat(f).st_mtime < time.time() - 20 * 60:
    if os.path.isfile(f):
      os.remove(f)
