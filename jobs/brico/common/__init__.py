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

from brico.common.memoize import memoized
import os
import sys
import time

@memoized
def pwd():      return os.path.dirname(sys.argv[0])

@memoized
def get_token(keyfile):
  with open( os.path.join( pwd(), ".keys", keyfile ) ) as x:
    return x.read().rstrip()

def write_pull(filename, list):
  filename = os.path.join( pwd(), "../html/pull", filename )
  list.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )

  file = open(filename + ".new", "wb")
  file.write( u"\n".join(list).encode("utf-8") )
  file.close()
  os.rename(filename + ".new", filename)
