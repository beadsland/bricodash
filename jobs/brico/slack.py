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

from slacker import Slacker
import emoji_data_python
from vend.memoize import memoized
import brico.common.thumb
import brico.common.html as html

import urllib.parse
import re

thumb = brico.common.thumb.Cache()
re_thumb = re.compile(r"/files-tmb/")

class Slack:
  def __init__(self, token):
    self.api = Slacker( token )
    self.token = token

  ###
  # Retrieve messages from a channel
  ###
  @memoized
  def messages(self, channel, count):
    history = self.history(channel = self.channels()[channel]['id'],
                           latest = None, oldest = 0, count = count)
    return history.body['messages']

  ###
  # Queries against result
  ###
  @memoized
  def members(self):            return self.api.users.list().body['members']

  @memoized
  def emoji(self, name=None):
    if not name:  return self.api.emoji.list().body['emoji']
    else:         return self.mojilink(name);

  # not memoized 'cause kwargs'
  def history(self, **kwargs):  return self.api.channels.history(**kwargs)

  ###
  # Generated lookup tables
  ###
  @memoized
  def channels(self):
    return { c['name']: c for c in self.api.channels.list().body['channels'] }

  @memoized
  def names(self, user=None):
    if not user:
      names = { u['id']: ( u['profile']['display_name'], u['name'] )
                                                    for u in self.members() }
      for id in names:
        names[id] = names[id][1] if names[id][0] == "" else names[id][0]
      return names
    else:
      return self.names()[user]

  @memoized
  def avatars(self, user=None):
    if not user:
      return { u['id']: u['profile']['image_32'] for u in self.members() }
    else:
      return html.logo( self.avatars()[user] )

  ###
  # Links
  ###
  @memoized
  def link(self, u, slemoji=False):
    parse = urllib.parse.urlparse(u)
    if (slemoji):
      return html.img().clss('slemoji').src( thumb.get(u) ).str()
    elif (parse.path.endswith( ('.gif', '.jpg', '.jpeg', '.png') )):
      headers = { "Authorization": "Bearer " + self.token }
      if (re_thumb.match(parse.path)):    file = thumb.get(u, headers)
      else:                               file = thumb.get_thumb(u)
      return html.logo(file)
    else:
      file = u if len(u) < 55 else "%s…%s" % (u[:30], u[-20:])
      return html.span().style("font-size: 75%;").inner("<%s>" % file).str()

  @memoized
  def mojilink(self, name):
    if name in self.emoji():
      if self.emoji()[name].startswith("alias:"):
        return self.mojilink( self.emoji()[name].replace("alias:", "") )
      else:
        return self.link( self.emoji()[name], True )
    else:
      return html.emoji( emoji_data_python.replace_colons(":%s:" % name) )
