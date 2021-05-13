#!/bin/bash
TZ=GMT0;
export TZ;

# Change encoding in tracks file
iconv -t UTF-8 -f ISO-8859-2 unique_tracks.txt > serialized.txt

# Part 1 of exercise - prepare star schema files hierarchy
## Remove track_id from tracks
sed -i -e $'s/<SEP>/\v/g' serialized.txt
cut -d $'\v' -f 2- serialized.txt > tracks.txt
rm serialized.txt

## Sort files and remove duplicates with song's details
sort --output=sorted_tracks.txt tracks.txt
uniq -i sorted_tracks.txt tracks_unique.txt
rm tracks.txt sorted_tracks.txt

## Iteration on large samples file and generate date file
gawk -F'<SEP>' '{
  year_month_day = strftime("%Y-%m-%d", $3);
  date[year_month_day] = 1
  print $1 "," $2 "," $3 "," year_month_day > "samples_formatted.txt"
}
END {
  n = asorti(date, indexes);
  for (i = 1; i <= n; i++) {
    split(indexes[i], array, "-");
    print indexes[i] "," array[1] "," array[2] "," array[3] > "dates.txt"
  }
}' triplets_sample_20p.txt

# Part 2 - run codes
chmod +x exercise_1.sh exercise_2.sh exercise_3.sh exercise_4.sh exercise_5.sh
./exercise_1.sh
./exercise_2.sh
./exercise_3.sh
./exercise_4.sh
./exercise_5.sh
