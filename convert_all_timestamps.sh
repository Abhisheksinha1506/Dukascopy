basepath=$(dirname $(dirname $(dirname $(realpath $0))))
cd $basepath

for file in $(find $basepath/data -type f)
  do
    python $basepath/resources/linux/utc_timestamp_convert.py -f $file
done
