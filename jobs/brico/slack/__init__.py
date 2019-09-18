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
from vend.multisub import multiple_replace

import brico.common.thumb
from brico.slack.slacker import Slack as BaseSlack
import brico.common.html as html

import urllib.parse
import re
import humanize
import datetime

def bold(str):  return "*%s*" % str
def ital(str):  return "_%s_" % str
def quot(str):  return ">%s" % str

thumb = brico.common.thumb.Cache()
re_thumb = re.compile(r"/files-tmb/")

###
# Outer formatting
###
def div(s): return html.div().clss("slacking").inner(s).str()
def usp(s): return html.span().clss("slacker").inner("@%s" % s).str()
def chn(s): return html.span().clss("slackchan").inner("#%s" % s).str()
def qut(s): return html.div().clss("slackquote").inner(s).str()

###
# Link, image and emoji formatting
##
@memoized
def slemoji(u): return html.img().clss('slemoji').src( u ).str()
def reactji(s): return html.div().clss('reactji').inner( s ).str()
def reactct(s): return html.span().clss('reactct').inner( s ).str()
def linky(u):
  file = u if len(u) < 40 else "%s…%s" % (u[:20], u[-15:])
  return html.span().clss('slink').inner("&lt;%s&gt;" % file).str()

emotags = { 'emotag': html.emoji, 'imgtag': html.logo, 'lnktag': linky,
            'slemotag': slemoji, 'reactdiv': reactji, 'reactct': reactct }

###
# Slack API wrapper
###
class Slack(BaseSlack):

  ###
  # Emoji
  ###
  def emoji(self, name=None, tags={}):
    if not name:  return self.app.emoji.list().body['emoji']
    else:         return self.mojilink(name, tags);

  # correctly handle combining characters
  @memoized
  def concat_emoji(self, str):
    tag = '<span class="emoji"\ >'
    patt = re.compile( "(%s[^<]+)</span>%s" % (tag, tag) )
    return patt.sub(r'\g<1>', str)

  ###
  # Format text and attachments part of message
  ###
  @memoized
  def txtdict(self):
    return [ ("^&gt; (.*)\n", lambda m: qut(m.group(1)) ),
             ("<(http[^>]+)>", lambda m: self.link(m.group(1), html.logo,
                                                   linky) ),
             ("<#[^\|>]+\|([^>]+)?>", lambda m: chn(m.group(1)) ),
             ("<@([^\|>]+)(\|[^>]+)?>", lambda m: usp(self.names(m.group(1))) ),
             (":([A-Za-z\-_0-9]+):", lambda m: self.emoji(m.group(1),
                                                          emotags) ) ]

  def format_text(self, message):
    text = message['text']
    for tup in self.txtdict(): text = re.compile(tup[0]).sub(tup[1], text)
    text = self.concat_emoji(text)
    if 'edited' in message:
      text += ' %s' % html.span().clss('sledited').inner("(edited)").str()
    text = ' '.join([ text,
                      ' '.join(self.attachments(message, html.logo, linky)),
                      ' '.join(self.reactions(message, emotags)) ])
    return text

  ###
  # Format timestamp as duration
  ###
  @memoized
  def durdict(self):
    return { "second": "sec", "minute": "min", "hour": "hr",
             "day": "dy", "week": "wk", " ago": "" }

  def human_time(self, ts):
    delta = datetime.datetime.now().timestamp() - float(ts)
    return multiple_replace( humanize.naturaltime(delta), self.durdict() )

  ###
  # Links
  ###
  @memoized
  def link(self, u, imgtag=None, lnktag=None, slemotag=None):
    parse = urllib.parse.urlparse(u)
    if (slemotag):
      return slemotag( thumb.get(u) )
    elif (parse.path.endswith( ('.gif', '.jpg', '.jpeg', '.png') )):
      headers = { "Authorization": "Bearer " + self.app_token }
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
          if 'author_icon' in file:
            if 'text' not in file: file['text'] = ""

            if 'service_name' in file:
              channel = file['service_name']
            else:
              channel = "#%s" % file['channel_name']

            footer = "(%s ago on %s)" % ( self.human_time(file['ts']),
                                           channel )
            footer = html.span().clss('sledited').inner(footer).str()
            quote = "%s: %s %s" \
                     % (html.logo(thumb.get(file['author_icon'])),
                        self.format_text(file), footer)
            return [ qut(quote) ]
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
