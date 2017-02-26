#!/bin/sh
if [ "X$1" = "X" ]; then
    echo "usage: `basename $0` <host>"
    exit 1
fi

if [ "X$SSH_AUTH_SOCK" = "X" ]; then
        eval `ssh-agent -s`
        ssh-add $HOME/.ssh/id_rsa
fi

AUTOSSH_POLL=20
AUTOSSH_PORT=$(awk 'BEGIN { srand(); do r = rand()*32000; while ( r < 20000 ); printf("%d\n",r)  }' < /dev/null)
#AUTOSSH_GATETIME=30
#AUTOSSH_LOGFILE=$HOST.log
#AUTOSSH_DEBUG=yes
#AUTOSSH_PATH=/usr/local/bin/ssh
#export AUTOSSH_POLL AUTOSSH_LOGFILE AUTOSSH_DEBUG AUTOSSH_PATH AUTOSSH_GATETIME AUTOSSH_PORT
export AUTOSSH_POLL

# -t is the ssh option to force a pseudo terminal (pty)
autossh -M $AUTOSSH_PORT -t $@ "tmux attach-session"
