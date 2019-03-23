#!/usr/bin/env python3

import re
import json
from urllib.parse import urlencode
from urllib.request import urlopen
import wikitextparser

import brico.common

API_URL = "https://wiki.hackmanhattan.com/api.php"

def main():
  cal = []
  for l in parse("Bricodash/Extra:Calendar").lists():
    for i in l.items:
      cal.append(i.lstrip())

  brico.common.write_text("extra.cal", cal)

def parse(title):
  data = {"action": "query", "prop": "revisions", "rvlimit": 1,
          "rvprop": "content", "format": "json", "titles": title}
  raw = urlopen(API_URL, urlencode(data).encode()).read()
  res = json.loads(raw)
  text = list(res["query"]["pages"].values())[0]["revisions"][0]["*"]
  return wikitextparser.parse(text)
