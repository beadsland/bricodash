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

  # not memoized because tags
  def emoji(self, name=None, tags={}):
    if not name:  return self.api.emoji.list().body['emoji']
    else:         return self.mojilink(name, tags);

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
  def avatars(self, user=None, tag=None):
    if not user:
      return { u['id']: u['profile']['image_32'] for u in self.members() }
    else:
      return self.link( self.avatars()[user], tag )

  ###
  # Links
  ###
  @memoized
  def link(self, u, imgtag=None, lnktag=None, slemotag=None):
    parse = urllib.parse.urlparse(u)
    if (slemotag):
      return slemotag( thumb.get(u) )
    elif (parse.path.endswith( ('.gif', '.jpg', '.jpeg', '.png') )):
      headers = { "Authorization": "Bearer " + self.token }
      if (re_thumb.match(parse.path)):    file = thumb.get(u, headers)
      else:                               file = thumb.get_thumb(u)
      return file if not imgtag else imgtag( file )
    else:
      return u if not lnktag else lnktag( u )

  # can't memoize because tags
  def mojilink(self, name, tags={}):
    if name in self.emoji():
      if self.emoji()[name].startswith("alias:"):
        return self.mojilink( self.emoji()[name].replace("alias:", ""), tags )
      else:
        return self.link( self.emoji()[name], None, None, tags['slemotag'] )
    else:
      emoji = emoji_data_python.replace_colons(":%s:" % name)
      return emoji if not 'emotag' in tags else tags['emotag']( emoji )

  # not memoized because message
  def attachments(self, message, imgtag=None, lnktag=None):
    text = []

    for key in ['files', 'attachments']:
      if key in message:
        for file in message[key]:
          for path in ['thumb_64', 'image_url', 'permalink']:
            if path in file:
              if file[path] not in message['text']:
                text.append( self.link(file[path], imgtag, lnktag) )
              break # for path

    return text

  def reactions(self, message, tags={}):
    if 'reactions' not in message: return ""
    text = []

    for r in message['reactions']:
      reaction = "%s%s" % (self.mojilink(r['name'], tags),
                           tags['reactct'](str(r['count'])))
      text.append( tags['reactdiv'](reaction) )

    return text
