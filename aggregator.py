#!/usr/local/bin python

import optparse
import sys
from datetime import *

def aggregate():
  p = optparse.OptionParser()
  p.add_option('--start', '-s', default="1900", type="int", help="Just aggregate data starting with this year.")
  p.add_option('--end', '-e', default="3000", type="int", help="Just aggregate data up to this year.")
  p.add_option('--limit_rows', '-l', default=None, type="int", help="Just parse a fixed number of rows.")
  p.add_option('--sep', '-p', default=",", help="Character that splits column in main")
  p.add_option('--fill', '-f', action="store_true", dest="fill", default=False, help="Fill missing months with zeroes.")
  p.add_option('--header', '-d', default=None, help="Specify header from a separate file.")
  p.add_option('--header_sep', default=",", help="Character to split header row.")
  options, arguments = p.parse_args()

  event_codes = map(str, range(1, 21))
  actor_types = ["MIL"]
  date_ix = None
  ix = 0
  counts = {}

  if options.header: 
    with open(options.header, 'rb') as f:
      headers = f.readline().replace(options.header_sep, " ").rstrip().split()
  else: 
    headers = []
  
  for line in sys.stdin:
    # Get the headers
    line = line.replace('"','').replace("\n", '').split(",")
    if len(headers) == 0:
      headers = line 
    if ix==0:
      date_ix = headers.index('date')
      actor1_geo_country_code_ix = headers.index('Actor1CountryCode')
      actor2_geo_country_code_ix = headers.index('Actor2CountryCode')
      actor1_type1_code_ix = headers.index('Actor1Type1Code')
      actor2_type1_code_ix = headers.index('Actor2Type1Code')
      root_code_ix = headers.index('EventRootCode')
      if not options.header: 
        ix += 1
        continue

    # Parse some dates
    this_date = datetime.strptime(line[date_ix], "%Y-%m-%d")
    country_1 = line[actor1_geo_country_code_ix]
    country_2 = line[actor2_geo_country_code_ix]
    actor_1_type = line[actor1_type1_code_ix]
    actor_2_type = line[actor2_type1_code_ix] 
    event_root_code = line[root_code_ix]
    # Is this in our window to aggregate?
    if this_date.year >= options.start and this_date.year <= options.end:

      # Lazy init hashes
      if this_date.year not in counts.keys():
        counts[this_date.year] = {}
      if this_date.month not in counts[this_date.year].keys():
        counts[this_date.year][this_date.month] = {}
      if country_1 not in counts[this_date.year][this_date.month].keys():
        counts[this_date.year][this_date.month][country_1] = {}
      if country_2 not in counts[this_date.year][this_date.month][country_1].keys():
        counts[this_date.year][this_date.month][country_1][country_2] = {}
        for event_code in event_codes:
          counts[this_date.year][this_date.month][country_1][country_2][event_code] = 0
        for actor_type in actor_types:
          counts[this_date.year][this_date.month][country_1][country_2][actor_type] = 0

      counts[this_date.year][this_date.month][country_1][country_2][event_root_code] += 1

      for actor_type in actor_types:
        if (actor_1_type == actor_type) or (actor_2_type == actor_type):
          counts[this_date.year][this_date.month][country_1][country_2][actor_type] += 1

    ix += 1
    if options.limit_rows and ix > options.limit_rows:
      break

    if options.fill:
      for year in counts.keys():
        for month in counts[year].keys():
          for country_1 in counts[year][month].keys():
            for country_2 in counts[year][month][country_1].keys():
              for event_code in event_codes:
                counts[year][month][country_1][country_2][event_code] = counts[year][month][country_1][country_2][event_code] or 0
              for actor_type in actor_types:
                counts[year][month][country_1][country_2][event_code] = counts[year][month][country_1][country_2][actor_type] or 0

  eventcodestr = ",".join('event' + i for i in event_codes)
  typestr = ",".join(['actor' + i for i in actor_types])
  col_names = "year,monthy,country_1,country_2," + eventcodestr + "," + typestr + "\n" 
  formatted_string = ",".join(["%s"] * (4 + len(event_codes) + len(actor_types))) + "\n"
  sys.stdout.write(col_names)
  for year in counts.keys():
    for month in counts[year].keys():
      for country_1 in counts[year][month].keys():
        for country_2 in counts[year][month][country_1].keys():
          data = tuple([year, month, country_1, country_2] + counts[year][month][country_1][country_2].values())
          sys.stdout.write(formatted_string % data)

if __name__ == '__main__':
  aggregate()