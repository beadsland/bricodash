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
import requests
import json

def shorten(url):
  token = brico.common.get_token("firebase_key")
  rest = "https://firebasedynamiclinks.googleapis.com/v1/shortLinks?"

  info = { "dynamicLinkDomain": "brico.page.link",
           "link": url }
  suff = { "option": "SHORT" }
  data = json.dumps( { "dynamicLinkInfo": info, "suffix": suff } )

  response = requests.post("%s%s" % (rest, token), data=data)
  if response.status_code != 200:   sys.exit(response.status_code);
  result = json.loads(response.text)
  return result['shortLink']
