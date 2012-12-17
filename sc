#!/bin/sh

if [ -f /etc/rc.d/$1 ]; then
	/etc/rc.d/$1 $2
elif [ -f /usr/local/etc/rc.d/$1 ]; then
	/usr/local/etc/rc.d/$1 $2
else
	echo "Cannout find service $1."
fi

