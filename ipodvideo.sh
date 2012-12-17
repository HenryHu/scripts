#!/bin/sh

if [ "$3" != "" ]; then
	ASPECT="-aspect $3"
else
	ASPECT=
fi

ffmpeg -i "$1" -f mov -vcodec libx264 -b 1000k -maxrate 10000k -acodec libfaac -ab 256k -s 720x480 $ASPECT "$2"


