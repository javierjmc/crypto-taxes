#!/usr/bin/python3 

import datetime
import argparse
import json
import sys
import urllib.request
from collections import defaultdict
import pprint

pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(prog='Process some integers.')
parser.add_argument('currency', metavar='CURRENCY', type=str)

args = parser.parse_args()

with open('data/trades-value/{0}.json'.format(args.currency)) as f:
  s = f.read()

  rows = json.loads(s)

value = 0
amount_total = 0
average_expense = 0

previous = defaultdict(float)

# see https://bt.cx/sv/news/2017/03/30/deklarationsdags-angest-har-du-salt-bitcoin/

for current in rows:
  current['value'] = current['amount'] * current['value'][args.currency]['SEK']

  current['amount_total'] = previous['amount_total'] + current['amount']

  if current['amount'] >= 0:
    current['expense_change'] = current['value']
  else:
    current['expense_change'] = previous['expense_average'] * current['amount']

  current['expense_unused'] = previous['expense_unused'] + current['expense_change']
  current['expense_average'] = current['expense_unused'] / current['amount_total']

  previous = current

summary = dict(
    gain=dict(value=0, expense=0, amount=0),
    loss=dict(value=0, expense=0, amount=0)
)

for current in rows:
  if current['value'] < 0:
    current['result'] = abs(current['value']) - current['expense_average']


    if current['result'] > 0:
      v = summary['gain']
    elif current['result'] < 0:
      v = summary['loss']

    v['value'] += abs(current['value'])
    v['expense'] += abs(current['expense_change'])
    v['amount'] += abs(current['amount'])

  else:
    current['result'] = 0.0
    
with open('data/trades-calculation/{0}.json'.format(args.currency), "w+") as f:
  s = json.dumps(rows)

  f.write(s)

with open('data/trades-summary/{0}.json'.format(args.currency), "w+") as f:
  s = json.dumps(summary)

  f.write(s)
