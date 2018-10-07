#!/usr/bin/env python3

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

# API License: https://creativecommons.org/licenses/by-sa/4.0/
# Data License: https://opendatacommons.org/licenses/odbl/

import brico.common
import brico.html
import json

# https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
def heat_index_rothfusz(T, RH):
  RH = RH/100
  HI = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH \
       - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH \
       + .00085282*T*RH*RH - .00000199*T*T*RH*RH
  if (RH < .13 and 80 <= T <= 112):
    HI = HI - ( (13-RH)/4 ) * sqrt( (17-abs(T-95.))/17 )
  elif (RH > .85 and 80 <= T <= 87):
    HI = HI + ( (RH-85)/10 ) * ( (87-T)/5 )
  return HI

def heat_index(T, RH):
  HI = 0.5 * ( T + 61.0 + ( (T-68.0)*1.2 ) + (RH*0.094) )
  return HI if HI >= 80 else heat_index_rothfusz(T, RH)

# https://www.weather.gov/epz/wxcalc_windchill
def wind_chill(T, WS):
  if T <= 50 and WS > 3:
    C = 35.74 + (0.6125 * T) - (35.75 * WS**0.16) + (0.4275 * T * WS**0.16)
    return C
  else:
    return T

condn = { '01d': "🌞", '02d': "🌤", '03d': "🌥", '04d': "☁☁",
          '01n': "🌝", '02n': "🌙☁", '03n': "☁", '04n': "☁☁",
          '09d': "🌦", '10d': "🌧", '11d': "⛈", '13d': "🌨",
          '09n': "🌧", '10n': "🌧", '11n': "⛈", '13n': "🌨",
          '50d': brico.html.img().clss('logo').src("img/fog.png").str(),
          '50n': brico.html.img().clss('logo').src("img/fog.png").str() }

def poll(zipcode):
  path = "http://api.openweathermap.org/data/2.5/weather"
  params = { "zip": zipcode, "units": "imperial" }
  token = brico.common.get_token("owm_key")
  response = brico.common.get_result(path, params, token)
  data = json.loads(response.text)

  w = {}

  w['condn'] = condn[data['weather'][0]['icon']]
  w['condn'] = brico.html.span().clss('emoji').inner(w['condn']).str()

  w['tempf'] = data['main']['temp']
  w['tempc'] = (w['tempf'] - 32) * 5/9

  w['winds'] = data['wind']['speed']
  w['chill'] = wind_chill(w['tempf'], w['winds'])

  w['humid'] = data['main']['humidity']
  w['index'] = heat_index(w['tempf'], w['humid'])

  w['tempf'] = round(w['tempf'])
  w['tempc'] = round(w['tempc'])
  w['chill'] = round(w['chill'])
  w['index'] = round(w['index'])

  return w
