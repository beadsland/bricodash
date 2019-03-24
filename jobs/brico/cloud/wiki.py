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

def main():
  query = "https://wiki.hackmanhattan.com/api.php?action=query&list=recentchanges&rcprop=title%7Cids%7Csizes%7Cflags%7Cuser%7Ctimestamp&rclimit=200&rcshow=!minor&format=json"
  response = requests.get(query)
  if response.status_code != 200:   sys.exit(response.status_code);
  result = json.loads(response.text)

  recent = result["query"]["recentchanges"]
  seen = []
  report = []
  wlogo = '<img class="logo" src="img/mediawiki.png">&thinsp;'

  for edit in recent:
    if edit["title"] not in seen:
      path = edit["title"].split("/")
      for i in range(len(path)):
        if path[i].find(":") > -1:
          path[i] = '<span class="wiki-special">' + path[i] + "</span>"
      title = wlogo + "/&#x200a;".join(path)
      html = '<div class="wiki-line">' + title + "</div>"
      report.append( (edit["timestamp"], html) )
      seen.append( edit["title"] )

  return report
