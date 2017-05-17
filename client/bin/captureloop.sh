#!/bin/bash

URL="$1"
USER="$2"
PASS="$3"

while true
do
  FILENAME=$(date +"%m_%d_%I_%M")
  RAWFILENAME="$FILENAME".mjpg
  MP4FILENAME="$FILENAME".mp4
  echo $FILENAME

  wget -O "$RAWFILENAME" --user "$USER" --password "$PASS" "$URL" &
  TASK_PID=$!
  sleep 120
  kill -9 "$TASK_PID"

  ffmpeg -i "$RAWFILENAME" "$MP4FILENAME"
  
  if [ -f "$MP4FILENAME" ]; then
    echo "Created $MP4FILENAME"
    rm -f "$RAWFILENAME" 
  else
    echo "Failed to create $MP4FILENAME"
    exit 1
  fi

done
