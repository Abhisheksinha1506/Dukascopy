## Abstract
In my exploration of world of big data and I became curious about tick data. Tick data is extremely granular and provides a great challenge for those looking to work on their optimization skills due to its size. Unfortunately, market data is almost always behind a pay wall or de-sampled to the point of uselessness. After discovering the Dukascopy api, I knew I wanted to make this data available for all in a more accessible format.

| Totals                  | Quantities      |
| :---                    | :----:          |
| Total Files             | 463             |
| Total Line Count        | 8,495,770,706   |
| Total Data Points       | 33,983,082,824  |
| Total Decompressed Size | 501 GB          |
| Total Compressed Size   | 61 GB           |

![Relations](https://i.imgur.com/AD2joeJ.png)


## File Formats
---------
The data was collected from https://www.dukascopy.com/ via a public api that allows for the download of tick data on the hour level. These files come in the form of a .bi5 file. Th

These files where decompressed, then merged into yearly CSV's named in the following convention. "AUDCHF\_tick\_UTC+0\_00\_2011.csv" or 'Pair\_Resolution\_Timezone\_Year.csv'

These CSV's are split into 3 categories "Majors", "Crosses", "Commodities"

Majors, Crosses, and Commodities have had their timestamps modified so that they are in the official UTC ISO standard. This was originally done for a Postgresql database that quickly became obsolesced. Any files that have been modified are appended with a "-Parse". These timestamps have been modified in the following format.

```
Millisecond timestamps to UTC +00:00 time
[2017.01.01 22:37:08.014] ----> [2017-01-01T22:37:08.014+00:00]
```

## User Resources
---------
For those looking to use this data in a live context or update it frequently, I have included a number of tools for both Windows and Linux that will be useful.

### Windows 
The `~/dukascopy/resources/windows` contains a third party tool written in java that can download and convert Dukascopy's .bi5 files. I have also included the latest zstd binaries from Zstandard Github page.

### Linux
Linux is my daily driver in 99% of cases, so I have developed all my scraping tools using linux only tools. In the `~/dukascopy/resources/linux` folder you will find a number of shell script and pyhton3 files that I used to collect this data. There are quite a few files in this directory but I will cover the core ones below.

#### download-day.py
This file is used to download a single symbol for a single day and then convert and merge all 24 .bi5 files it into a single csv.

#### download-year.py
This file is used to download a single symbol for a full year and then convert and merge all .bi5 files it into a single csv.

#### dukascopy.py
This file contains all the core logic for downloading and converting data from dukascopy.

#### utc-timestamp-convert.py
This tad slow but works well enough. It requires the pandas project and parses timestamps into the UTC ISO standard. This is useful for those looking to maintain the format of new files with the those in this repo, or those looking to use this in a SQL database.
