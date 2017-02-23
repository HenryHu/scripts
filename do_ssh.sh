#!/bin/sh

# $1: key file
# $2: server
# $3: user

if [ "$3" = "" ]; then
    echo "usage: $0 <key.pub> <server> <user>"
    exit 2
fi

echo Copy SSH key
scp $1 $2:otherkey.pub

echo Check for existence
if ssh $2 sudo test -e /home/$3/.ssh/authorized_keys; then
    echo Target file already exists.
    if ssh $2 sudo diff /home/$3/.ssh/authorized_keys otherkey.pub; then
        echo "Target file matches new file."
    else
        ssh $2 "sudo sh -c \"cat otherkey.pub >> /home/$3/.ssh/authorized_keys\""
    fi
    ssh $2 rm otherkey.pub
else
    echo Create authorized_keys
    if ssh $2 sudo test ! -e /home/$3/.ssh; then
        ssh $2 sudo mkdir /home/$3/.ssh
    fi
    ssh $2 sudo mv otherkey.pub /home/$3/.ssh/authorized_keys
fi

echo Set permission \& owner
ssh $2 sudo chmod 700 /home/$3/.ssh
ssh $2 sudo chmod 644 /home/$3/.ssh/authorized_keys
ssh $2 sudo chown -R $3:$3 /home/$3/.ssh

echo Finished.
ssh $2 sudo ls -ld /home/$3/.ssh
ssh $2 sudo ls -l /home/$3/.ssh/authorized_keys
ssh $2 sudo cat /home/$3/.ssh/authorized_keys
