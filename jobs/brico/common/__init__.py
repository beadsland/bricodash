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

from vend.memoize import memoized
import os
import sys
import time
import urllib.parse
import requests
import json
import grp

###
# Locale constants
###

def lat():      return 40.7380441
def lon():      return -73.9984966
def city():     return "New York"

###
# System constants
###

@memoized
def pwd():      return os.path.dirname(sys.argv[0])

@memoized
def gid():      return grp.getgrnam("hmweb").gr_gid

@memoized
def pull():     return os.path.join( pwd(), "../html/pull" )

###
# API access
###
@memoized
def get_token(keyfile):
  with open( os.path.join( pwd(), ".keys", keyfile ) ) as x:
    return x.read().rstrip()

def get_response(path, params={}, token="", etag=None, bail=True):
  question = "&".join([ urllib.parse.urlencode(params), token ])
  if etag is not None:  headers = { 'If-None-Match': etag }
  else:                 headers = {}
  response = requests.get( "?".join([path, question]), headers=headers )
  if response.status_code == 304 and etag is not None:
    return response
  elif response.status_code != 200:
    write_pull("error.dump", [response.text])
    if bail:
      sys.exit(response.status_code)
  return response

###
# File operations
###
def touch(f):
  with open(f, 'a'):    os.utime(f, None)

def slurp(filename):
  filename = os.path.join( pull(), filename )
  with open(filename) as x: f = x.read()
  return f

def write_text(filename, list):
  filename = os.path.join( pull(), filename )

  file = open(filename + ".new", "wb")
  file.write( u"\n".join(list).encode("utf-8") )
  file.close()
  os.rename(filename + ".new", filename)

def write_pull(filename, list):
  list.append( '<span id="timestamp" epoch="' + str(time.time()) + '"></span>' )
  write_text(filename, list)

def write_json(filename, struct):
  filename = os.path.join( pull(), filename )
  if type(struct) is dict:
    struct['epoch'] = str(time.time())

  file = open(filename + ".new", "w")
  file.write( json.dumps(struct) )
  file.close()
  os.rename(filename + ".new", filename)
