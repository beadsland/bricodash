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

import json
from urllib.parse import urlencode
from urllib.request import urlopen
import wikitextparser

import brico.common

API_URL = "%s/api.php" % brico.common.wiki()

def parse(title):
  data = {"action": "query", "prop": "revisions", "rvlimit": 1,
          "rvprop": "content", "format": "json", "titles": title}
  raw = urlopen(API_URL, urlencode(data).encode()).read()
  res = json.loads(raw)
  text = list(res["query"]["pages"].values())[0]["revisions"][0]["*"]
  return wikitextparser.parse(text)

def recent():
  props = ['title', 'flags', 'user', 'timestamp']
  params = { 'action': "query", 'list': "recentchanges",
              'rcprop': "|".join(props),
              'rclimit': "200", 'rcshow': "!minor", 'format': "json" }
  response = brico.common.get_response(API_URL, params)
  result = json.loads(response.text)
  return result["query"]["recentchanges"]
