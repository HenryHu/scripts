#!/bin/sh


TPATH=/usr/local/share/WyabdcRealPeopleTTS/

#SENT="anyone hear me"
#SENT="test remote sound play"
#SENT="test remote sound play"
#SENT="now the volume should be lower"
#SENT="now the volume should be lower lower lower"
#SENT="one five eight one zero eight five eight four two four"
#SENT="my name as hen ray who"
#SENT="hey don make me cry"
SENT="big brother as watch in you"
ERR=0

for i in $SENT; do
	FIRST=`echo $i | head -c 1`
	FPATH=$TPATH/$FIRST/$i.wav
	if [ ! -e $FPATH ]; then
		echo No $TPATH/$FIRST/$i.wav
		ERR=1
	fi

done

FILES=''

if [ "$ERR" = "0" ]; then
	echo OK

	for i in $SENT; do
		FIRST=`echo $i | head -c 1`
		FPATH=$TPATH/$FIRST/$i.wav
		if [ ! -e $FPATH ]; then
			echo No $TPATH/$FIRST/$i.wav
			ERR=2
		else
			FILES="$FILES $FPATH"
		fi

	done


fi

mplayer -really-quiet $FILES
