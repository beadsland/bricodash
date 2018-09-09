#!/usr/bin/env python

import requests;
import json;

r = requests.get('http://web.mta.info/status/serviceStatus.txt')

if r.status_code == 200:
  

