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

import re

import brico.common.html

def line(s):
  return brico.common.html.div().clss("cloud-line").inner(s).str()

def special(s):
  return brico.common.html.span().clss("cloud-special").inner(s).str()

###
# Shrink special parts of titles (Wiki namespaces, repository usernames)
# to reduce necessity of line-wrapping. Also, provide for line-breaks on
# embedded title delimiters (slashes and colons).
###
hairspace = "&#x200a;"
unsticky_slash = "/%s" % hairspace
unsticky_colon = ":%s" % hairspace

def super(s):
  return brico.cloud.special( brico.common.html.elem("sub").inner(s).str() )

def format_title(s):
  path = s.split("/")
  for i in range(len(path)):
    if path[i].find(":") > -1:
      path[i] = unsticky_colon.join( path[i].split(":") )
      path[i] = brico.cloud.special(path[i])
    elif len(path) > 1 and i == 0:
      path[i] = brico.cloud.special(path[i])

    path[i] = re.sub(r"(\([0-9]{1,2})\-([0-9]{1,2}\))",
                     lambda m: super("%s/%s" % (m[1], m[2])), path[i] )

  return unsticky_slash.join(path)
