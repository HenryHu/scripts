#!/usr/bin/env python

import subprocess
import time
import logging


def get_window_list(window_class):
    try:
        output = subprocess.check_output('xdotool search --onlyvisible --class %s' %
                                         window_class, shell=True)
        return output.strip().split()
    except:
        return []


def window_large_enough(window_id, width, height):
    output = subprocess.check_output('xdotool getwindowgeometry --shell %s' % window_id,
                                     shell=True)
    for line in output.strip().split('\n'):
        if '=' not in line:
            continue
        (name, val) = line.split('=')
        if name == 'WIDTH':
            if int(val) < width:
                return False
        if name == 'HEIGHT':
            if int(val) < height:
                return False
    return True


def any_window_large_enough(window_list, width, height):
    for window_id in window_list:
        if window_large_enough(window_id, width, height):
            return True
    return False


def delay_screensaver():
    logging.debug("delaying screen saver")
    subprocess.call('xscreensaver-command --deactivate', shell=True)
    subprocess.call('qdbus org.freedesktop.ScreenSaver /ScreenSaver SimulateUserActivity',
                    shell=True)
    subprocess.check_output('xset -dpms', shell=True)


def restore_screensaver():
    subprocess.check_output('xset +dpms', shell=True)


def get_proc_list(signature):
    try:
        output = subprocess.check_output('pgrep %s' % signature, shell=True)
        return output.strip().split('\n')
    except:
        return []


def using_more_cpu(pid, percent):
    try:
        output = subprocess.check_output('ps -p %s -o %%cpu=' % pid, shell=True)
        return float(output) > percent
    except:
        return False


def any_proc_using_cpu(proc_list, percent):
    for proc in proc_list:
        if using_more_cpu(proc, percent):
            return True
    return False


def run_check():
    window_list = get_window_list('npviewer.bin') + get_window_list('pluginloader.exe')
    if any_window_large_enough(window_list, 640, 480):
        proc_list = get_proc_list('npviewer.bin') + get_proc_list('wine')
        if any_proc_using_cpu(proc_list, 15):
            delay_screensaver()
        else:
            logging.debug("no proc using cpu")
            restore_screensaver()
    else:
        logging.debug("no window large enough")
        restore_screensaver()


def run_loop(check_interval):
    while True:
        run_check()
        time.sleep(check_interval)

if __name__ == "__main__":
    debug = False
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        CHECK_INTERVAL = 1
    else:
        logging.basicConfig(level=logging.INFO)
        CHECK_INTERVAL = 60

    run_loop(CHECK_INTERVAL)
