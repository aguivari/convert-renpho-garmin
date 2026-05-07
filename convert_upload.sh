#!/bin/bash

if [ -z "$1" ];
then
  echo "needed arguments: <CSV file to process> <scale brand> <gender>"
  exit 1
fi

filename="$(date +%Y%m%d%H%M%S).fit"
directory=$(dirname "$1")

real_path=$(realpath "${BASH_SOURCE[0]}")
script_dir=$(dirname "$real_path")

python "${script_dir}/convert-scale-garmin.py" "$2" "$1" "$directory/$filename"  "$3"
python "${script_dir}/uploader.py" "$directory/$filename"

