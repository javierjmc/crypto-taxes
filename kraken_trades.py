#!/usr/bin/python3

import csv

from itertools import groupby
import pprint
import re

from collections import defaultdict

import datetime

import json

pp = pprint.PrettyPrinter(indent=4)

with open('data/kraken_trades.csv' ,'r') as f:
    data_iter = csv.reader(f, 
                           delimiter = ',', 
                           quotechar = '"')
    csv = [data for data in data_iter]

names = { v: k for (k,v) in enumerate(csv[0]) }

data = csv[1:]

groups = groupby(data, lambda row: row[names['ordertxid']])

items = []

re1 = re.compile(r'X(...)Z(...)')
re2 = re.compile(r'(...)(...)')

for _, group in groups:
  group = list(group)

  pair = group[0][names['pair']]

  m1 = re1.match(pair)
  m2 = re2.match(pair)

  # buy: acquire the first currency, relinquish the second
  # sell: acquire the second currency, relinquish the first

  # in the below we use the following terminology
  # resource - what you receive buying or selling (ETH typically)
  # currency - what you use for buying and selling (EUR typically)

  if m1 is not None:
    (resource_symbol, currency_symbol) = m1.groups()
  elif m2 is not None:
    (resource_symbol, currency_symbol) = m2.groups()
  else:
    raise Exception(pair)

  currency_volume = sum([ float(row[names['cost']]) for row in group ])
  resource_volume = sum([ float(row[names['vol']]) for row in group ])

  mode = group[0][names['type']]

  if mode == "sell":
    source = (resource_symbol, resource_volume)
    target = (currency_symbol, currency_volume)
  elif mode == "buy":
    source = (currency_symbol, currency_volume)
    target = (resource_symbol, resource_volume)
  else:
    raise Exception(mode)

  time = datetime.datetime.strptime(group[0][names['time']], "%Y-%m-%d %H:%M:%S.%f").isoformat()

  items.append(dict(
    time=time,
    source=source,
    target=target
  ))


resources = defaultdict(list)

for item in items:
  source = item['source']
  target = item['target']

  resource = resources[source[0]]
  resource.append(dict(time=item['time'], amount=-source[1]))

  resource = resources[target[0]]
  resource.append(dict(time=item['time'], amount=target[1]))

for (k,rows) in resources.items():
  with open("data/trades/{0}.json".format(k), "w+") as f:
    s = json.dumps(rows)
    f.write(s)
