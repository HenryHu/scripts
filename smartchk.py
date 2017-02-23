#!/usr/bin/env python2

import json
import re
import subprocess
import sys

cfgfile = "/home/henryhu/scripts/smart.json" if len(sys.argv) < 2 else sys.argv[1]

servers = json.loads(open(cfgfile).read())

sigs = {
        "Reallocated_Sector" : "Reallocated Sector Count",
        "Current_Pending" : "Current Pending Sector Count",
        "Offline_Uncorrect" : "Offline Uncorrectable Sector Count"
        }

def run_smart(name, disk, args):
    if ":" in disk:
        (dev, devtype) = disk.split(":")
        return subprocess.check_output("ssh %s sudo /usr/sbin/smartctl -d %s /dev/%s %s" % (name, devtype, dev, args), shell=True)
    else:
        return subprocess.check_output("ssh %s sudo /usr/sbin/smartctl /dev/%s %s" % (name, disk, args), shell=True)

has_error = False

for server in servers:
    name = server["name"]
    if "test" in server:
        test_type = server["test"]
    else:
        test_type = None
    for disk in server["disk"]:
        #print "disk %s on server %s:" % (disk, name)
        try:
            try:
                smartdata = run_smart(name, disk, '-a')
            except subprocess.CalledProcessError as e:
                if not e.output:
                    raise e
                smartdata = e.output
            for sig in sigs:
                match = re.search("%s.*\s+(\d+)\n" % sig, smartdata)
                if match is None:
                    continue
                value = int(match.group(1))
                if value != 0:
                    print "WARNING: %s = %d for disk [%s] on server [%s]" % (sigs[sig], value, disk, name)
                    has_error = True
            if test_type is not None:
                for match in re.findall("Background %s\s+([^\s]+)" % test_type, smartdata):
                    # XXX "Self" : "Self test in progress"
                    if match != "Completed" and match != "Self":
                        print "WARNING: %s test result is %s for disk [%s] on server [%s]" % (test_type, match, disk, name)
                        has_error = True
                        # it's normal for multiple error entries
                        break
                for match in re.findall("%s offline\s+([^\s]+)" % (test_type[0].upper() + test_type[1:]), smartdata):
                    # XXX "Self-test" : "Self-test in progress"
                    if match != "Completed" and match != "Self-test" and match != "Interrupted" and match != "Aborted":
                        print "WARNING: %s test result is %s for disk [%s] on server [%s]" % (test_type, match, disk, name)
                        has_error = True
                        # it's normal for multiple error entries
                        break
        except Exception as e:
            print "WARNING: Exception %r occoured checking disk [%s] on server [%s]" % (e, disk, name)
            has_error = True

        if test_type is not None:
            try:
                run_smart(name, disk, '-t %s' % test_type)
            except subprocess.CalledProcessError as e:
                # it's possible that the test is already running
                if not "remaining" in e.output:
                    print "WARNING: Exception %r occoured running %s test on disk [%s] on server [%s]" % (e, test_type, disk, name)
                    has_error = True

if has_error:
    sys.exit(1)
