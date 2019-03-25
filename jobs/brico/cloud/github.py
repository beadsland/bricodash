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
import sys
import time

import brico.cloud
import brico.common.thumb
import brico.common.html

thumb = brico.common.thumb.Cache()

def main():
  glogo = "%s%s" % (brico.common.html.logo("img/github.png"), '&thinsp;')

  seen = []
  report = []

  for n in ["beadsland"]:
    result = get_events(n)
    if result:
      push = result[0]
      repo = brico.cloud.format_title(push["repo"]["name"])
  #    avatar = thumb.get_thumb(get_user(n)["avatar_url"])
  #    title = ''.join([ glogo, brico.common.html.logo(avatar), repo ])
      title = ''.join([ glogo, repo ])
      html = brico.cloud.line(title)
      report.append( (push["created_at"], html) )

  for p in range(1,10):
    result = get_events("hackmanhattan", "hm", p)

    for push in result:
      if push["repo"]["name"] not in seen:
        repo = brico.cloud.format_title(push["repo"]["name"])
        title = ''.join([ glogo, repo ])
        html = brico.cloud.line(title)
        report.append( (push["created_at"], html) )
        seen.append( push["repo"]["name"] )

  brico.common.write_json("github.json", report)
  return report

def get_user(user):
  query = "https://api.github.com/users/%s" % user
  cache = "github_%s_user.json" % user

  return get_result(query, cache)

###
# Request a page of events
###
def get_events(user, short=None, page=1):
  query = "https://api.github.com/users/%s/events?page=%d" % (user, page)

  if short is None:  cache = "github_%s.json" % user
  else:              cache = "github_%s_%02d.json" % (short, page)

  return get_result(query, cache)

###
# Query an API using using Etags to cache and respecting X-Poll-Interval
###
def get_result(query, cache):
  try:
    old = json.loads(brico.common.slurp(cache))
    etag = old['etag']
  except:
    etag = None

  response = brico.common.get_response(query, etag=etag, bail=False)
  if response.status_code == 304:
    result = old['result']
  elif response.status_code == 200:
    result = json.loads(response.text)
    etag = response.headers['ETag']
    save = { 'etag': etag, 'result': result }
    brico.common.write_json(cache, save)
  else:
    result = None

  try:     sleep = int(response.headers['X-Poll-Interval'])
  except:  sleep = 1
  time.sleep(sleep)

  return result
