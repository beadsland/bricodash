#!/usr/bin/env python

import os
import time
import sys

pwd = os.path.dirname(sys.argv[0])
pid = os.path.join(pwd, "pid")

for i in range(1, 240):
  list = [ f for f in os.listdir(pid) if f.startswith("l") ]
  list = [ (os.path.join(pid, f.replace("l", "c")), os.path.join(pid, f)) for f in list ]
  list = [ t for t in list if os.path.isfile(t[0]) ]
  list = [ (os.path.getmtime(t[0]), os.path.getmtime(t[1])) for t in list ]
  list = [ (t[1]-t[0], time.time()-t[1]) for t in list ]

  result = []
  for t in list:
    live = 60 / ( t[0] + .0001 )
    if t[1] < 1.1:
      result.append( live )
    else:
      dead = 2 / ( t[1] + .0001 )
      result.append( min([dead, dead * live, live]) )

  result = str(sum(result))
  result = '<span id="veil" value="' + result + '"></span>'
  result += '<span id="timestamp" epoch="' + str(time.time()) + '"></span>'

  filename = os.path.join(pwd, "../../html/pull/sous.html")

  file = open(filename + ".new", "w")
  file.write( result )
  file.close()
  os.rename(filename + ".new", filename)

  time.sleep(.25)

#  time.sleep(5)

for f in os.listdir(pid):
  f = os.path.join(pid, f)
  if os.stat(f).st_mtime < time.time() - 20 * 60:
    if os.path.isfile(f):
      os.remove(f)
