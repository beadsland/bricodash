#!/usr/bin/env python3

import astral
import ephem
import datetime
import pytz

def sunset(date, city):
  a = astral.Astral()
  a.solar_depression = 'civil'
  city = a[city]
  sun = city.sun(date=date, local=True)

  return sun['sunset'].astimezone(pytz.UTC)

minelong = ephem.degrees("8:0:0")

city = "Miami"

date = datetime.date(2019, 5, 4)
obs = ephem.city(city)
obs.date = sunset(date, city)
m = ephem.Moon(obs)
elong = m.elong
s = ephem.Sun(obs)
print(elong, m.alt, s.alt, ephem.degrees(m.alt - s.alt))

date = datetime.date(2019, 6, 3)
obs = ephem.city(city)
obs.date = sunset(date, city)
m = ephem.Moon(obs)
elong = m.elong
s = ephem.Sun(obs)
print(elong, m.alt, s.alt, ephem.degrees(m.alt - s.alt))

import dateutil.parser
earlst = dateutil.parser.parse('2019/06/03 00:00:00 +1400')
latest = dateutil.parser.parse('2019/06/04 00:00:00 -1200')
print(earlst, latest)
earlst = earlst.astimezone(pytz.UTC)
latest = latest.astimezone(pytz.UTC)
print(earlst, latest)

half = (latest - earlst) /2
while ephem.Moon(earlst).elong < ephem.degrees("8:0:0") \
    and half > datetime.timedelta(seconds=0):
  half = (latest - earlst) /2

  while ephem.Moon(earlst + half).elong > ephem.degrees("8:0:0"):
#    print("inner", earlst+half, ephem.Moon(earlst + half).elong, half)
    half = half / 2

  print(earlst, ephem.Moon(earlst).elong, half)
  earlst = earlst + half

print(earlst, ephem.Moon(earlst).elong)
print(latest - earlst)

s = ephem.Sun(earlst)
print(earlst, "solar declination", s.dec)

# Known:
#  * bounded datetime range of just under 11 hours, 40 minutes
#  * only sunset matters for any given location
#  * stop as soon as we find any location with delta altitude >= 5

# Assuming a perfectly spherical Earth, sunset at any given time happens
# over a topological curve from pole to pole.
#
# Can we assume that our altitude delta floor is only found on a contiguous
# segment of that curve?




#import datetime

#now = datetime.datetime.now() - datetime.timedelta(days=0)

#import brico.events.lunar.muslim

#printed = False
#for e in brico.events.lunar.muslim.main(now):
#  if now.isoformat() < e['start'] and not printed:
#    print(now)
#    printed = True
#  print(e)
