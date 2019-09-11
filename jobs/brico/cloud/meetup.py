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

import brico.cloud
import brico.common
import brico.common.html
import brico.common.meetup
import brico.common.gallery

gallery = brico.common.gallery.Line()

import datetime

def main():
  recent = brico.common.meetup.events(brico.common.group(), 100)
  edits = [ (e['updated']/1000, e['local_date'], e['name']) for e in recent ]
  edits = [ { 'timestamp': e[0], 'date': e[1], 'title': e[2] } for e in edits ]
  edits = sorted(edits, key = lambda e: e['date'])
  edits = sorted(edits, key = lambda e: e['timestamp'], reverse=True)

  seen = []
  report = []
  mlogo = "%s%s" % (brico.common.html.logo("img/meetup.png"), '&thinsp;')

  for e in edits:
    if e['title'] not in seen:
      nums = e['date'][5:].split("-")
      month = nums[0].lstrip("0")
      day = nums[1].lstrip("0")
      date = "(%s-%s)" % (month, day)

      title = ' '.join([ elide_title( e['title'] ), date ])
      title = ''.join([ mlogo, brico.cloud.format_title(title) ])
      report.append( (datetime.datetime.fromtimestamp(e["timestamp"]).isoformat(),
                      title) )
      seen.append( e["title"] )

  photos = brico.common.meetup.photos(brico.common.group())
  photos = reversed(sorted(photos, key = lambda p: p['created']))
  for i in photos:
    created = datetime.datetime.fromtimestamp(i['created']/1000).isoformat()
    gallery.push(i['thumb_link'], created)

  report.append( (gallery.timestamp, ''.join([ mlogo, gallery.str() ]) ))

  report = sorted(report)[-10:]
  brico.common.write_json("meetup_edits.json", report)
  return report

def elide_title(title):
  words = title.split(" ")
  title = ""
  while len(title) < 15 and len(words) > 0:
    title = " ".join([ title, words.pop(0) ])
  if len(words) > 0:
    title = "".join([ title, "…" ])
  return title[1:]
