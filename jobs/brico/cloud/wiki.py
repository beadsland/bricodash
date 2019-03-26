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

import requests
import json

import brico.cloud
import brico.common.html
import brico.common
import brico.common.wiki

def main():
  recent = brico.common.wiki.recent()
  seen = []
  report = []
  wlogo = "%s%s" % (brico.common.html.logo("img/mediawiki.png"), '&thinsp;')

  for edit in recent:
    if edit["title"] not in seen:
      title = ''.join([ wlogo, brico.cloud.format_title(edit["title"]) ])
      html = brico.cloud.line(title)
      report.append( (edit["timestamp"], html) )
      seen.append( edit["title"] )

  brico.common.write_json("wiki.json", report)
  return report
