#!/usr/bin/env python3

import subprocess
import time

def get_result_from_command(cmd):
    result = subprocess.check_output(cmd)
    result = result.decode('utf-8')
    result = result.strip()
    return result

def get_result_from_sysctl(node):
    return get_result_from_command(["sysctl", "-n", node])

def get_result_from_bsdsensors(sensor):
    #return get_result_from_command(["sudo", "bsdsensors", "-sensors", sensor])
    return ""

def get_max_cpu_freq_from_pcm():
    subprocess.check_output(['pcm-core', '0.5', '-csv=/tmp/pcm.csv', '-i=1'])
    period = 500
    max_freq = 0
    for line in open("/tmp/pcm.csv", "r"):
        line = line.strip()
        if line.startswith('Time elapsed'):
            period = int(line.split(':')[1].strip().split(' ')[0])
        if line.endswith(','):
            parts = line.split(',')
            cpu_num = parts[0]
            if cpu_num == '*': continue
            cycles = float(parts[3])
            freq = cycles / period
            max_freq = max(max_freq, freq)

    return int(max_freq / 1000)

def get_max_cpu_freq():
    try:
        return get_max_cpu_freq_from_pcm()
    except:
        return ''

def get_cpu_temp():
    return get_result_from_sysctl("dev.cpu.0.temperature").rstrip('C')

def get_mb_temp():
    try:
        return get_result_from_sysctl("hw.acpi.thermal.tz0.temperature").rstrip('C')
    except:
        return get_result_from_bsdsensors("temp:SYSTIN")


def get_gpu_temp():
    try:
        return get_result_from_command(["nvidia-settings", "-q", "0/GPUCoreTemp", "-t"])
    except:
        return None

def get_freq_str(name, freq):
    if not freq:
        return ''
    if freq > 1000:
        return "%s: %.2fG" % (name, freq / 1000.0)
    return "%s: %sM" % (name, freq)

def get_temp_color(temp):
    if temp >= 90:
        return "red"
    elif temp >= 80:
        return "magenta"
    elif temp >= 70:
        return "magenta"
    elif temp >= 60:
        return "yellow"
    elif temp >= 50:
        return "blue"
    elif temp >= 40:
        return "blue"
    elif temp >= 30:
        return "cyan"
    else:
        return "green"

def get_temp_str(name, temp):
    if not temp:
        return ''
    try:
        temp_val = float(temp)
        temp_color = get_temp_color(temp_val)
        return "#[fg=white]%s: #[fg=%s]%.1fC#[fg=default]" % (name, temp_color, temp_val)
    except:
        return "%s: %sC" % (name, temp)

def get_time_str():
    curdate = time.strftime("%Y/%-m/%-d")
    curtime = time.strftime("%H:%M:%S")
    return "#[default]#[fg=green]%s #[fg=blue]%s#[default]" % (curdate, curtime)


cpu_freq = get_max_cpu_freq()
cpu_temp = get_cpu_temp()
mb_temp = get_mb_temp()
gpu_temp = get_gpu_temp()

cpu_freq_str = get_freq_str("CPU", cpu_freq)
cpu_temp_str = get_temp_str("CPU", cpu_temp)
mb_temp_str = get_temp_str("MB", mb_temp)
gpu_temp_str = get_temp_str("GPU", gpu_temp)
time_str = get_time_str()
print("%s %s" % (' '.join(filter(lambda x: x, [cpu_freq_str, cpu_temp_str, mb_temp_str, gpu_temp_str])), time_str))

