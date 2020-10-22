#!/usr/bin/env python3

# utc_timestamp_convert.py
#
# Convert Dukascopy milisecond timestamps to UTC +00:00 time
# I.E. [2017.01.01 22:37:08.014] ----> [2017-01-01T22:37:08.014+00:00]
#
# 1. Add headers to each csv. UTCtime,AskPrice,BidPrice,AskVolume,BidVolume
# 2. Convert First 3 "." with "-" in column 1
# 3. Repalce space with "T" in column 1
# 4. Append "+00:00" on the end of column 1
# 5. Export New CSV
# 6. Remove Old CSV

import os
import argparse
import pandas as pd


def parse_tick_downloader_csv(source):
    if os.path.exists(source) is False:
        print(source + ' Was NOT Found!')
        return

    if source.endswith('.gz') or source.endswith('.zst') or source.endswith('.zip'):
        print('Cannot Convert Compressed Files!')
        return

    if source.endswith('-Parse.csv'):
        print(source + ' Was Already Parsed!')
        return

    export_path = source[:-4] + '-Parse.csv'
    print('Reading Source CSV ' + source.split('/')[-1] + '...')
    df = pd.read_csv(source, error_bad_lines=False)

    print('Parsing Source CSV...')
    df.columns = ['UTC', 'AskPrice', 'BidPrice', 'AskVolume', 'BidVolume']
    df.UTC = df.UTC + '+00:00'
    df[['UTC', 'timetemp']] = df['UTC'].str.split(' ', expand=True)
    df.UTC.replace('\.', '-', inplace=True, regex=True)
    df.UTC = df.UTC + 'T' + df.timetemp
    df.drop(['timetemp'], axis=1, inplace=True)

    print('Exporting Parsed CSV to ' + export_path.split('/')[-1] + '...')
    df.to_csv(export_path, index=False)
    del df
    print('Finished Parsing CSV!')
    print('Removing Source File!')
    os.remove(source)
    print('')


parser = argparse.ArgumentParser(description="Convert Dukascopy milisecond timestamps to UTC +00:00 time.")
parser.add_argument("-f", "--file", metavar=('/full/file/path'), help="Full file path of CSV to convert.")
args = parser.parse_args()

if args.file:
    parse_tick_downloader_csv(args.file)
