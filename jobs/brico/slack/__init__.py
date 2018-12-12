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

import emoji_data_python
from vend.memoize import memoized
import brico.common.thumb
from brico.slack.slacker import Slack as BaseSlack

import urllib.parse
import re

def bold(str):  return "*%s*" % str
def ital(str):  return "_%s_" % str
def quot(str):  return ">%s" % str

thumb = brico.common.thumb.Cache()
re_thumb = re.compile(r"/files-tmb/")

class Slack(BaseSlack):

  ###
  # Emoji
  ###
  def emoji(self, name=None, tags={}):
    if not name:  return self.api.emoji.list().body['emoji']
    else:         return self.mojilink(name, tags);

  # correctly handle combining characters
  @memoized
  def concat_emoji(self, str):
    tag = '<span class="emoji"\ >'
    patt = re.compile( "(%s[^<]+)</span>%s" % (tag, tag) )
    return patt.sub(r'\g<1>', str)

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
          for path in ['thumb_64', 'thumb_url', 'image_url', 'permalink']:
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
