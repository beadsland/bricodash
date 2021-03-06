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

import time
import re
import json

import brico.cloud
import brico.common.thumb
import brico.common.html

thumb = brico.common.thumb.Cache()

def hubpush(r): return True if 'type' in r.keys() \
                           and r['type'] == "PushEvent" else False
def labpush(r): return True if 'action_name' in r.keys() \
                           and r['action_name'] == "pushed to" else False

def main():
  hub_logo = "%s%s" % (brico.common.html.logo("img/github.png"), '&thinsp;')
  lab_logo = "%s%s" % (brico.common.html.logo("img/gitlab.png"), '&thinsp;')

  repos = []
  for l in brico.common.wiki.parse("Bricodash/Extra:Repos").lists():
    for i in l.items:
      r = re.compile("#.*$").sub("", i).split("::")
      repos.append( ( r[0].rstrip().lstrip(), r[1].rstrip().lstrip() ) )

  seen = []
  report = []
  for n in repos:
    result = get_events(n[0], n[1])
    if result is not None:
      while len(result) > 0:
        if not (hubpush(result[0]) or labpush(result[0])):
          result.pop(0)
        else:
          push = result.pop(0)
          if n[1] == "github":
            repo = brico.cloud.format_title(push["repo"]["name"])
            title = ''.join([ hub_logo, repo ])
      #    avatar = thumb.get_thumb(get_user(n)["avatar_url"])
      #    title = ''.join([ glogo, brico.common.html.logo(avatar), repo ])
          elif n[1] == "gitlab":
            name = get_project_path(n[0], n[1], push["project_id"])
            repo = brico.cloud.format_title(name)
            title = ''.join([ lab_logo, repo ])
          else:
            continue  # just move on if bad service name
          if title not in seen:
            report.append( (push["created_at"], title) )
            seen.append( title )

  for p in range(1,10):
    result = get_events("hackmanhattan", "github", "hm", p)

    for push in result:
      if hubpush(push) and push["repo"]["name"] not in seen:
        repo = brico.cloud.format_title(push["repo"]["name"])
        title = ''.join([ hub_logo, repo ])
        report.append( (push["created_at"], title) )
        seen.append( push["repo"]["name"] )

  brico.common.write_json("github.json", sorted(report))
  return report

###
# Request user info to obtain avatar -- EXPERIMENTAL
###
def get_user(user):
  query = "https://api.github.com/users/%s" % user
  cache = "github_%s_user.json" % user

  return get_result(query, cache)

###
# Request a page of events
###
def get_events(user, serv="github", short=None, page=1):
  if serv == "github":
    query = "https://api.github.com/users/%s/events?page=%d" % (user, page)
  elif serv == "gitlab":
    query = "https://gitlab.com/api/v4/users/%s/events" % (user)
  else:
    return None

  if short is None:  cache = "%s_%s.json" % (serv, user)
  else:              cache = "%s_%s_%02d.json" % (serv, short, page)

  return get_result(query, cache, serv)

###
# Request gitlab project name
###
def get_project_path(user, serv, proj):
  query = "https://gitlab.com/api/v4/projects/%s" % (proj)
  cache = "%s_%s_%s.json" % (serv, user, proj)
  result = get_result(query, cache, serv)
  return result["path_with_namespace"]

###
# Query an API using using Etags to cache and respecting X-Poll-Interval
###
def get_result(query, cache, serv):
  cache = re.sub(r'[^A-Za-z0-9-_\.\/]', '', cache)

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

  try:
    sleep = int(response.headers['X-Poll-Interval'])
  except:
    if serv == "gitlab":
      sleep = 6 # gitlab throttles at 10 hits / minute
                # per @mkozono
                # https://gitlab.com/gitlab-org/gitlab-ce/issues/41308
    else:
      sleep = 1
  time.sleep(sleep)

  return result
