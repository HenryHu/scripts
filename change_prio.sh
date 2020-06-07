#!/bin/sh

extrahiprio="-20"
hiprio="-10"
loprio="20"

change_prio() {
    proc=$1
    prio=$2
    pids=`pgrep -x $proc`
    for pid in $pids; do
        nice=`ps -o nice $pid | tail -n 1`
        if [ "$nice" != "$prio" ]; then
            sudo renice $prio $pid
            logger "Changing priority of $pid ($proc) to $prio"
        fi
    done
}

top_prio() {
    proc=$1
    change_prio $proc $extrahiprio
}

raise_prio() {
    proc=$1
    change_prio $proc $hiprio
}

drop_prio() {
    proc=$1
    change_prio $proc $loprio
}

while true; do
    # Top prio: system services
    top_prio pulseaudio
    top_prio Xorg
    top_prio plasmashell
    top_prio kwin_x11
    top_prio latte-dock
    top_prio fcitx
    top_prio fcitx5
    top_prio dbus-daemon
    top_prio bthidd
    top_prio synergy-core

    # Top prio: terminal
    top_prio tmux
    top_prio st

    # High prio: browser
    raise_prio firefox

    # Low prio: computational tasks
    drop_prio make
    drop_prio "c\+\+"
    drop_prio clang
    drop_prio "clang\+\+"

    sleep 1;
done
