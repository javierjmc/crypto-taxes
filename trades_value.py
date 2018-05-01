#!/usr/bin/python3 

import datetime
import argparse
import json
import  sys
import urllib.request

parser = argparse.ArgumentParser(prog='Process some integers.')
parser.add_argument('currency', metavar='CURRENCY', type=str)

args = parser.parse_args()

URL_FORMAT="https://min-api.cryptocompare.com/data/pricehistorical?fsym={currency}&tsyms=SEK,EUR&ts={timestamp}&extraParams=ukarlsson_taxes"

with open('data/trades/{0}.json'.format(args.currency)) as f:
  s = f.read()

  rows = json.loads(s)

for row in rows:
  time = datetime.datetime.strptime(row['time'], "%Y-%m-%dT%H:%M:%S.%f")

  url = URL_FORMAT.format(currency=args.currency, timestamp=int(time.timestamp()))
  
  row['value'] = json.loads(urllib.request.urlopen(url).read())


with open('data/trades-value/{0}.json'.format(args.currency), "w+") as f:
  s = json.dumps(rows)

  f.write(s)
