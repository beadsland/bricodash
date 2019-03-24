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
  query = "https://api.github.com/users/hackmanhattan/events?page="

  seen = []
  report = []
  glogo = '<img class="logo" src="img/github.png">&thinsp;'


  for p in range(1,10):
    response = requests.get(query + str(p))
    if response.status_code != 200:   sys.exit(response.status_code);
    result = json.loads(response.text)
    for push in result:
      if push["repo"]["name"] not in seen:
        repo = push["repo"]["name"].replace("hackmanhattan/", "")
        title = glogo + repo
        html = '<div class="cloud-line">' + title + "</div>"
        report.append( (push["created_at"], html) )
        seen.append( push["repo"]["name"] )

  return report
