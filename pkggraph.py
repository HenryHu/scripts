#!/usr/bin/env python

import subprocess
import sys

sys.stdout = open('%s.dot' % sys.argv[1], 'w')

def query_one(root):
    query_multiple([root])

def query_multiple(items):
    visited = set(items)
    queue = items
    qh = qe = 0
    while qh <= qe:
        for qi in xrange(qh, qe + 1):
            item = queue[qi]
#            print "visiting", item
            deps = subprocess.check_output('pkg query %%dn %s' % item, shell=True).split('\n')
            for dep in deps:
                if not dep:
                    continue
                print '\t"%s" -> "%s";' % (item, dep)
                if dep in visited:
                    continue
                queue += [dep]
                visited.add(dep)
        qh = qe + 1
        qe = len(queue) - 1


def query_all():
    for line in subprocess.check_output('pkg query -a %n', shell=True).split('\n'):
        if not line:
            continue
        pkg = line

        deps = subprocess.check_output('pkg query %%dn %s' % pkg, shell=True).split('\n')
        for dep in deps:
            if not dep:
                continue
            print '\t"%s" -> "%s";' % (pkg, dep)

print "digraph G {"

query_multiple(sys.argv[1:])

print "}"

sys.stdout.close()

subprocess.check_call("dot -Tpng -o %s.png %s.dot" % (sys.argv[1], sys.argv[1]), shell=True)
subprocess.check_call("xdg-open %s.png" % sys.argv[1], shell=True)
