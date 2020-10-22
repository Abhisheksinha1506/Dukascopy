#!/usr/bin/env python3

import argparse
import dukascopy

parser = argparse.ArgumentParser(description="This file is used to download a single symbol for a full year and then convert and merge all .bi5 files it into a single csv.")
parser.add_argument("-y", "--year", help="Year to download and convert")
parser.add_argument("-sym", "--symbol", help="Spesify symbol to download")
parser.add_argument("-d", "--dir", default=False, help="Set a directory for downloads")
parser.add_argument("-o", "--out_dir", default=False, help="Set a directory for file output")
args = parser.parse_args()


if args.symbol and args.year:
    if args.dir is False:
        working_dir = '/tmp/dukascopy/working/' + args.symbol.upper()
    else:
        working_dir = args.dir

    if args.out_dir is False:
        out_dir = '/tmp/dukascopy/'
    else:
        out_dir = args.out_dir + '/' + str(args.year)

    dukascopy.download_sym(args.symbol, args.year, working_dir)
    dukascopy.merge_to_year(working_dir, out_dir, args.symbol, args.year)
