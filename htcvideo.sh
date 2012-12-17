#!/bin/sh

if [ "$3" != "" ]; then
	ASPECT="-aspect $3"
else
	ASPECT=
fi

ffmpeg -i "$1" -f mp4 -vcodec libx264 -b 2000k -threads 0 -acodec libfaac -ab 256k -ar 48000 -s 800x480 $ASPECT "$2"
# -coder 0: disable CABAC
# -bf 0: disable B frames
#ffmpeg -i "$1" -f mp4 -vcodec libx264 -vpre fast -vpre main -b 2000k -bf 0 -coder 0 -threads 0 -acodec libfaac -ab 256k -ar 48000 -s 800x480 $ASPECT "$2"

# only diff: weightp = 0 in baseline, weightp = 2 in main(default)
#ffmpeg -i "$1" -f mp4 -vcodec libx264 -vpre fast -vpre baseline -b 2000k -threads 0 -acodec libfaac -ab 256k -ar 48000 -s 800x480 $ASPECT "$2"


