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

def large_enough(width, height):
    def func(window_id):
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
        logging.debug("large %s", window_id)
        return True
    return func

def fullscreen():
    def func(window_id):
        output = subprocess.check_output('xprop -id %s _NET_WM_STATE' % window_id, shell=True)
        if 'FULLSCREEN' in output:
            logging.debug("fullscreen! %s", window_id)
            return True
        else:
            return False
    return func

def title_contains(text):
    def func(window_id):
        output = subprocess.check_output('xprop -id %s WM_NAME' % window_id, shell=True)
        title = output.split('=')[1].strip()
        if text in title:
            logging.debug("text %s in %s! (%s)", text, title, window_id)
            return True
        else:
            return False
    return func

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

def any_window(window_list, func):
    for window_id in window_list:
        if func(window_id):
            return True
    return False

def run_check():
    window_list = get_window_list('npviewer.bin') + get_window_list('pluginloader.exe')
    if any_window(window_list, large_enough(640, 480)):
        proc_list = get_proc_list('npviewer.bin') + get_proc_list('wine')
        if any_proc_using_cpu(proc_list, 15):
            delay_screensaver()
            return
        else:
            logging.debug("large window, no cpu")
    else:
        logging.debug("no large window")

    window_list = get_window_list('Firefox')
    if (any_window(window_list, fullscreen()) or
        any_window(window_list, title_contains("YouTube")) or
        any_window(window_list, title_contains("bilibili")) or
        any_window(window_list, title_contains("BiliPlus"))):
        proc_list = get_proc_list('firefox')
        if any_proc_using_cpu(proc_list, 15):
            delay_screensaver()
        else:
            logging.debug("fullscreen or video player, no cpu")
    else:
        logging.debug("no fullscreen")

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
