#!/usr/bin/env python2

import argparse
import subprocess
import sys

def run_cmd(cmd):
    ret = subprocess.Popen(cmd, shell=True)
    ret.communicate()
    if ret.returncode != 0:
        print "ERROR: %d" % ret.returncode
        sys.exit(ret.returncode)

class AptBackend(object):
    def available(self):
        return subprocess.call("dpkg -h", shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    def search(self, args):
        name = args.args[0]
        run_cmd("apt-cache search %s --names-only" % name)

    def install(self, args):
        name = args.args[0]
        run_cmd("sudo apt-get install %s" % name)

    def update(self, args):
        run_cmd("sudo apt-get update")

    def upgrade(self, args):
        run_cmd("sudo apt-get dist-upgrade")

    def which(self, args):
        path = args.args[0]
        run_cmd("dpkg -S %s" % path)

    def files(self, args):
        name = args.args[0]
        run_cmd("dpkg-query -L %s" % name)

    def list(self, args):
        run_cmd("dpkg -l")

class PacmanBackend(object):
    def available(self):
        return subprocess.call("pacman -h",
                               shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    def search(self, args):
        name = args.args[0]
        run_cmd("pacman -Q %s" % name)

    def install(self, args):
        name = args.args[0]
        run_cmd("sudo pacman -S %s" % name)

    def update(self, args):
        run_cmd("sudo pacman -Sy")

    def upgrade(self, args):
        run_cmd("sudo pacman -Su")

    def which(self, args):
        path = args.args[0]
        run_cmd("pacman -Qo %s" % path)

    def files(self, args):
        name = args.args[0]
        run_cmd("pacman -Ql %s" % name)

    def list(self, args):
        run_cmd("pacman -Q")

class PkgBackend(object):
    def available(self):
        return subprocess.call("pkg help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

    def search(self, args):
        name = args.args[0]
        run_cmd("pkg search %s" % name)

    def install(self, args):
        name = args.args[0]
        run_cmd("sudo pkg install %s" % name)

    def update(self, args):
        run_cmd("sudo pkg update")

    def upgrade(self, args):
        run_cmd("sudo pkg upgrade")

    def which(self, args):
        path = args.args[0]
        run_cmd("pkg which %s" % path)

    def files(self, args):
        name = args.args[0]
        run_cmd("pkg info -l %s" % name)

    def list(self, args):
        run_cmd("pkg info")

backends = [AptBackend(), PacmanBackend(), PkgBackend()]

def detect_backend():
    for backend in backends:
        if backend.available():
            return backend
    return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    parser.add_argument("args", help="arguments", action='append', default=[], nargs='?')

    args = parser.parse_args()

    backend = detect_backend()
    if not backend:
        print "No backend available"
        sys.exit(1)

    if args.cmd == "search":
        backend.search(args)
    elif args.cmd == "install":
        backend.install(args)
    elif args.cmd == "update":
        backend.update(args)
    elif args.cmd == "upgrade":
        backend.upgrade(args)
    elif args.cmd == "which":
        backend.which(args)
    elif args.cmd == "files":
        backend.files(args)
    elif args.cmd == "list":
        backend.list(args)

if __name__ == "__main__":
    main()
