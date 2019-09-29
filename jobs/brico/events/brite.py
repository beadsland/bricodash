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
import eventbrite
import urllib.parse
import dateutil
import difflib

import brico.events
import brico.common
import brico.common.html as html
from brico.common.short import shorten
from vend.multisub import multiple_replace

###
# Collect events from our noisy neighbors
###
def main():
  brite = Brite()
  tenants = [ "Offside Tavern", "Secret Loft" ]
  replace = { "at %s" % t: "" for t in tenants }
  ratpark = []

  upmeet = brico.events.load_cals( ["upmeet.json"] )

  for event in brite.events(tenants):
    venue = brite.venue(event)

    if venue['name'] in tenants:
      start = event['start']['local']
      name = multiple_replace(event['name']['text'], replace).strip()

      isup = ""
      for up in upmeet:
        if name[:25] == up['event'][:25] \
            and dateutil.parser.parse(start) == dateutil.parser.parse(up['start']):
          isup = brico.common.html.logo("img/meetup.png", ":meetup:")
          name = common(name, up['event'])
          upmeet.remove(up)
          brico.common.write_json("upmeet.json", upmeet)
          break

      name = brico.events.noisy( brico.events.polite(name) )

      line = { "start": event['start']['local'],
               "venue": venue['name'],
               "event": "%s %s %s" % (name, short(event['url']), isup) }
      ratpark.append( line )

  brico.common.write_json( "brite.json", brico.events.datesort(ratpark)[:5] )

###
# Match common string parts
###
def common(str1, str2):
  str1 = "%s " % str1
  str2 = "%s " % str2
  parts = []
  l1 = 0
  l2 = 0

  while len(str1) > 0 and len(str2) > 0:
    m = longest(str1, str2)
    if m.size < 3 or " " not in str1[m.a:m.size]:         break
    parts.append(str1[m.a:m.a+m.size].lstrip().rstrip())
    str1 = " %s" % str1[m.a+m.size:]
    str2 = " %s" % str2[m.b+m.size:]

  return '…'.join(parts).rstrip()

def longest(str1, str2):
  matcher = difflib.SequenceMatcher(None, str1, str2, autojunk=False)
  return matcher.find_longest_match(0, len(str1), 0, len(str2))

###
# API wrapper class
###
class Brite:
  def __init__(self):
    token_file = os.path.join(brico.common.pwd(), ".keys/eventbrite_token")
    with open(token_file) as x: token = x.read().rstrip()
    self.api = eventbrite.Eventbrite(token)
    self.venues = {}

  def events(self, tenants):
    query = { 'location.address': "137 West 14th Street, New York, NY",
              'location.within': "1km",
              'sort_by': "date" }
    evts = []

    for t in tenants:
      query['q'] = t
      route = "/events/search?%s" % urllib.parse.urlencode(query)
      result = self.api.get( route )
      evts += result['events']
    return evts

  def venue(self, event):
    vid = event['venue_id']
    if vid not in self.venues:
      self.venues[vid] = self.api.get('/venues/%s' % vid)
    return self.venues[vid]

###
# Short event links provided to comply with Eventbrite API license
###
def linky(href, str):
  return html.a().clss('linky').href(href).target('_blank').inner(str).str()

def short(url):
  h = shorten(url).replace("https://", "", 1).split("/")
  return html.span().clss('thiny').inner(linky(url, "%s/" % h[0])).str() \
         + html.span().clss('shorty').inner(linky(url, h[1])).str()
