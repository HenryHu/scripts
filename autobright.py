#!/usr/bin/env python

import subprocess
import time

#100 77 60 48 42 37 30 25 18 12 5
LEVELS = {100000: (100, 100),
           10000: (75, 48),
            1000: (50, 37),
             100: (25, 25),
              -1: (10, 12)}

HISTORY_LEN = 5

def get_bright():
    return int(subprocess.check_output(["sysctl", "-n", "hw.acpi.asus_als.light"]))

def set_bright(state, level):
    (value1, value2) = LEVELS[level]
    state['last_level'] = level
    subprocess.check_call(["sudo", "ddccontrol", "-r", "0x10", "-w", str(value1),
                        "dev:/dev/iic2"])
    subprocess.check_call(["sudo", "sysctl",
                            "hw.acpi.video.lcd0.brightness=%d" % value2])

def most_appeared(array):
    stat = {}
    for data in array:
        stat[data] = stat.get(data, 0) + 1
    return max(stat, key=lambda k: stat[k])

def auto_brightness():
    state = {'last_level': -1}
    history = []

    while True:
        bright = get_bright()
#        print(bright)

        level_to_be = 0
        for level in LEVELS:
            if bright > level:
                level_to_be = level
                break

        if len(history) > HISTORY_LEN - 1:
            history = history[1:]
        history.append(level_to_be)

        level = most_appeared(history)
        doit = False
        last_level = state['last_level']
        if last_level != -1:
            if level > last_level:
                if bright > last_level * 3:
                    doit = True
            elif level < last_level:
                if bright < last_level * 0.7:
                    doit = True
        else:
            doit = True
        if doit:
            set_bright(state, level)
        time.sleep(1)

if __name__ == "__main__":
    auto_brightness()
