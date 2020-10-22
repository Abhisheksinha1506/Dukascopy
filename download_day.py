#!/usr/bin/env python3

import argparse
import dukascopy

parser = argparse.ArgumentParser(description="This file is used to download a single symbol for a single day and then convert and merge all 24 .bi5 files it into a single csv.")
parser.add_argument("-d", "--dir", default=False, help="Set a directory for downloads")
parser.add_argument("-dt", "--date", help="Set a date to download and convert")
parser.add_argument("-sym", "--symbol", help="Spesify symbol to download")
args = parser.parse_args()

if args.symbol and args.date:
    if args.dir is False:
        out_dir = '/tmp/dukascopy/working/' + args.symbol.upper() + '/' + str(args.date)
    else:
        out_dir = args.dir + '/' + str(args.date)

    dukascopy.fetch_day(args.symbol, args.date, out_dir)
