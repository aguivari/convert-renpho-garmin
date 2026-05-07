#!/bin/bash

if [ -z "$1" ];
then
  echo "needed arguments: <CSV file to process> <scale brand> <gender>"
  exit 1
fi

filename="$(date +%Y%m%d%H%M%S).fit"
directory=$(dirname "$1")

python ~/My\ Stuff/learning/convert-scale-garmin/convert-scale-garmin.py "$2" "$1" "$directory/$filename"  "$3"
python ~/My\ Stuff/learning/convert-scale-garmin/uploader.py "$directory/$filename"

