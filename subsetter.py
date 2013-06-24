#!/usr/local/bin python

import optparse
import sys
from datetime import *

def subset():
  p = optparse.OptionParser()
  p.add_option('--start', '-s', default="1900", type="int", help="Just subset data starting with this year.")
  p.add_option('--end', '-e', default="3000", type="int", help="Just subset data up to this year.")
  p.add_option('--limit_rows', '-l', default=None, type="int", help="Just parse a fixed number of rows.")
  p.add_option('--sep', '-p', default="\t", help="Character that splits column in main")
  p.add_option('--header', '-d', default=None, help="Specify header from a separate file.")
  p.add_option('--header_sep', default="\t", help="Character to split header row.")
  p.add_option('--country1', default=None, help="Country desired in Actor1CountryCode column.")
  p.add_option('--country2', default=None, help="Country desired in Actor2CountryCode column.")
  p.add_option('--geo1', default=None, help="Geography desired in Actor1Geo_CountryCode column.")
  p.add_option('--geo2', default=None, help="Geography desired in Actor2Geo_CountryCode column.")
  p.add_option('--quad_class', default=None, help="Quad Class codes (comma seperated")

  options, arguments = p.parse_args()

  date_ix = None
  ix = 0

  if options.header:
    with open(options.header, 'rb') as f:
      headers = f.readline().replace(options.header_sep, " ").rstrip().split()
  else:
    headers = []

  # Parse quad param
  quad_classes = None
  if options.quad_class:
    quad_classes = options.quad_class.split(",")

  for line in sys.stdin:
    # Get the headers
    tmp_line = line.replace('"','').replace("\n", '').split(options.sep)
    if len(headers) == 0:
      headers = tmp_line
    if ix == 0:
      date_ix = headers.index('SQLDATE')
      actor1_country_code_ix = headers.index('Actor1CountryCode')
      actor2_country_code_ix = headers.index('Actor2CountryCode')
      geo_1_code_ix = headers.index('Actor1Geo_CountryCode')
      geo_2_code_ix = headers.index('Actor2Geo_CountryCode')
      quad_class_ix = headers.index('QuadClass')
      if not options.header:
        ix += 1
        continue

    # Parse dates and actors
    this_date = datetime.strptime(tmp_line[date_ix], "%Y%m%d")

    country_1 = tmp_line[actor1_country_code_ix]
    country_2 = tmp_line[actor2_country_code_ix]
    geo_1 = tmp_line[geo_1_code_ix]
    geo_2 = tmp_line[geo_2_code_ix]
    quad_class = tmp_line[quad_class_ix]

    # Does this match our criteria for the subset?
    filter_out = False
    if this_date.year < options.start and this_date.year > options.end:
    	filter_out = True

    if options.country1 and country_1 != options.country1:
      filter_out = True

    if options.country2 and country_2 != options.country1:
      filter_out = True

    if options.geo1 and geo_1 != options.geo1:
      filter_out = True

    if options.geo2 and geo_2 != options.geo2:
      filter_out = True

    if quad_classes:
      if not quad_class in quad_classes:
        filter_out = True

    if not filter_out:
      sys.stdout.write(line)

if __name__ == '__main__':
  subset()