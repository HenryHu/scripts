import sys
import subprocess
import re

part_re = re.compile("\s+([0-9a-f]+):\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)\s+([0-9a-f]+)")

def get_list(name=None, filename=None):
    if filename is not None:
        out = subprocess.check_output(["fc-query", filename]).decode('utf-8')
    elif name is not None:
        out = subprocess.check_output(["fc-match", "-v", name]).decode('utf-8')
    inside = False
    charlist = []
    for line in out.split('\n'):
        if 'charset:' in line:
            inside = True
        if 'lang:' in line:
            inside = False
        if inside:
            if part_re.match(line):
                ret = part_re.match(line).groups()
                area = int(ret[0], 16)
                for i in range(8):
                    section = int(ret[i+1], 16)

                    for idx in range(32):
                        if section & (1 << idx):
                            pos = area * 256 + i * 32 + idx
                            charlist.append(pos)

    return charlist

def print_list(charlist, show_char=True):
    outcnt = 0
    for pos in charlist:
        print("%04x %c" % (pos, chr(pos)), end=' ')
        outcnt += 1
        if outcnt % (16 if show_char else 32) == 0:
            print()

    print()

target = None
pattern = ''
if len(sys.argv) > 1:
    if sys.argv[1][0] == '_':
        target = sys.argv[1][1:]
        if len(target) > 1:
            target = list(filter(lambda x: ord(x) > 255, list(target)))

        if len(sys.argv) > 2:
            pattern = sys.argv[2]
    elif sys.argv[1][0] == '#':
        target = chr(int(sys.argv[1][1:], 16))

        if len(sys.argv) > 2:
            pattern = sys.argv[2]
    else:
        for font in sys.argv[1:]:
            print_list(get_list(font))
        sys.exit(0)

if target:
    print("finding", target)

if target == '':
    print("no char!")
    sys.exit(0)

out = subprocess.check_output(["fc-list", ":", "family", "file"]).decode('utf-8')
for line in out.split('\n'):
    line = line.strip()
    if not line:
        break
    family = line.split(':')[1]
    filename = line.split(':')[0]
    charlist = get_list(name=family, filename=filename)
    if target is None:
        print("chars of %s (%s)" % (family, filename))
        print_list(charlist)
    else:
        for char in target:
            if ord(char) in charlist:
                print("char %c (%x) in %s (%s)" % (char, ord(char), family, filename))

for char in target:
    if not pattern:
        patterns = ('', 'monospace', 'sans-serif', 'serif')
    else:
        patterns = (pattern,)

    for pattern in patterns:
        my_pattern = pattern + ':charset=%x' % ord(char)
        out = subprocess.check_output(["fc-match", my_pattern]).strip()
        print("font for %c (%x) [%s]: %s" % (char, ord(char), pattern, out.decode('utf-8')))
