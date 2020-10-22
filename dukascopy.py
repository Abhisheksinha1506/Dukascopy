#!/usr/bin/env python3

import os
import lzma
import time
import struct
import shutil
import pandas as pd
from datetime import timedelta, date


def scan_dir(path):
    files = set()
    for x in os.scandir(path):
        if x.is_file():
            files.add(x.path)

    return files


def bi5_to_csv(date_ts, out_dir, files):
    print('Starting Coversion of All .bi5 Files...')

    sort = sorted(files)
    chunk_size = struct.calcsize('>3i2f')
    data = []

    for bi5 in sort:

        try:
            size = os.path.getsize(bi5)
        except (IOError, OSError):
            break

        if size > 0:
            with lzma.open(bi5) as f:
                while True:
                    chunk = f.read(chunk_size)
                    if chunk:
                        data.append(struct.unpack('>3i2f', chunk))
                    else:
                        break

        os.remove(bi5)

    if not data:
        print('All Downloaded Files Where Empty!')
        return 1

    df = pd.DataFrame(data)
    df.columns = ['UTC', 'AskPrice', 'BidPrice', 'AskVolume', 'BidVolume']
    df.AskPrice = df.AskPrice / 100000
    df.BidPrice = df.BidPrice / 100000
    df.UTC = pd.TimedeltaIndex(df.UTC, 'ms')
    df.UTC = df.UTC.astype(str)
    df.UTC = df.UTC.replace(regex=['0 days'], value=[str(date_ts)])
    df.UTC = df.UTC.str[:-3]

    df.to_csv(out_dir + '/daily.csv', index=False)
    print('Finished Converting Files!')
    return 0


def download(url, out_dir):
    try:
        os.system('wget -q ' + url + ' -P ' + out_dir)
    except Exception:
        pass


def fetch_day(pair, date, out_dir):
    baseurl = "http://datafeed.dukascopy.com/datafeed/"
    timestamps = {date + "/" + h for h in {str(n).zfill(2) for n in range(0, 24)}}

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    print('Downloading Source Files for ' + pair.upper() + ' on ' + date + '...')
    for t in timestamps:
        url = baseurl + pair + "/" + t + "h_ticks.bi5"
        download(url, out_dir)
        time.sleep(.1)

    if scan_dir(out_dir):
        print('Finished Download!')
    else:
        print('No Files Were Downloaded')
        shutil.rmtree(out_dir)
        return

    dt = date.split('/')
    date_ts = dt[0] + '.' + str(int(dt[1]) + 1).zfill(2) + '.' + dt[2]
    status = bi5_to_csv(date_ts, out_dir, scan_dir(out_dir))
    if status == 1:
        shutil.rmtree(out_dir)
        return
    os.rename(out_dir + '/daily.csv', os.path.dirname(out_dir) + '/' + date_ts + '.csv')
    shutil.rmtree(out_dir)


def create_date_list(year):
    dates = set()

    def daterange(date1, date2):
        for n in range(int((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    start_dt = date(int(year), 1, 1)
    end_dt = date(int(year), 12, 31)

    for dt in daterange(start_dt, end_dt):
        tmp_dt = dt.strftime("%Y/%m/%d")
        tmp_dt = tmp_dt.split('/')
        fdate = str(str(tmp_dt[0]).zfill(2) + '/' + str(int(tmp_dt[1]) - 1).zfill(2) + '/' + str(tmp_dt[2]).zfill(2))
        dates.add(fdate)

    return sorted(dates)


def download_sym(ticker, year, working_dir):
    dl_dates = create_date_list(year)
    for d in dl_dates:
        fetch_day(ticker, d, working_dir + '/' + d)
        print('----------------------------------------------------')


def merge_to_year(working_dir, out_dir, ticker, year):
    files = sorted({os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(working_dir)) for f in fn})
    print('Starting to Merge ' + str(len(files)) + ' Files...')
    df = pd.DataFrame(columns=['UTC', 'AskPrice', 'BidPrice', 'AskVolume', 'BidVolume'])

    for f in files:
        tmp_df = pd.read_csv(f, error_bad_lines=False)
        df = df.append(tmp_df)

    fname = ticker.upper() + '_tick_UTC+0_00_' + year + '.csv'
    print('Done Merging Files!')
    print('Exporting Data Now...')
    df.to_csv(out_dir + '/' + fname, index=False)
    print('Exported Data to ' + fname)
    shutil.rmtree(working_dir)
