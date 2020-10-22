# Get Repo Stats

basepath=$(dirname $(dirname $(dirname $(realpath $0))))
cd $basepath

echo "Starting To Get File Stats..."

rm -f file_stats.txt
rm -f file_stats.tmp1
rm -f file_stats.tmp2

for file in $(find $basepath/dukascopy/data -type f)
  do
    wc_stats=$(zstdcat $file | wc -lc)
    c_size=$(du -h $file)
    echo "$wc_stats $c_size" >> file_stats.tmp1
    echo "Finished Getting Stats on $(basename $file)"
done

echo "Parsing Raw Output..."

echo "File_Name Line_Count Decompressed_Size Compressed_Size" > file_stats.tmp2

cat file_stats.tmp1 | while IFS=' ' read lines bytes hread
do
  lc=$lines
  ds=$(numfmt --to=iec $bytes)
  cs=$(echo "$hread" | awk -F '[\t]' '{print $1}')
  file=$(basename $(echo "$hread" | awk -F '[\t]' '{print $2}'))
  echo "$file $lc $ds $cs" >> file_stats.tmp2
done

cat file_stats.tmp2 | column -t > file_stats.txt

rm -f file_stats.tmp1
rm -f file_stats.tmp2

echo "Finished Fetching File Stats!"
echo "Results in $basepath/file_stats.txt"
