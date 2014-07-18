import time
import sys
import signal
import atexit

def out(s):
    sys.stdout.write(s)

def flush():
    sys.stdout.flush()

def run(width, delay, before='.', after='_', middle='orz'):
    def print_result():
        out('\nround: %d\n' % round)
    def handler(signum, frame):
        atexit.register(print_result)
        sys.exit(0)

    signal.signal(signal.SIGALRM, handler)
    left = 0
    right = width - len(middle)
    round = 0

    while True:
#        out('\b' * (1 + len(str(round))))
        round += 1
        if left >= 0:
            out(before * left)
            out(middle)
        else:
            out(middle[-left:])
        if right > 0:
            out(after * right)
        if left < 0:
            out(middle[:-left])
#        out(' %d' % round)
        left -= 1
        if left >= 0:
            right += 1
        if left == -len(middle):
            left = width - len(middle)
            right = 0
            (before, after) = (after, before)

        flush()
        time.sleep(delay)
        out('\b' * width)

if __name__ == "__main__":
    signal.alarm(5)
    run(100, 0.000)
