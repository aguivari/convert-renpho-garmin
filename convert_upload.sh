#!/bin/bash

if [ -z "$1" ];
then
  echo "needed arguments: <scale brand> <gender> <CSV file to process>"
  exit 1
fi

filename="$(date +%Y%m%d%H%M%S).fit"
directory=$(dirname "$3")

real_path=$(realpath "${BASH_SOURCE[0]}")
script_dir=$(dirname "$real_path")

python "${script_dir}/convert-scale-garmin.py" "$1" "$3" "$directory/$filename" "$2"
python "${script_dir}/uploader.py" "$directory/$filename"

