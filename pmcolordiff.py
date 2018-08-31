#!/usr/bin/env python3
"""
    A simplistic version of colordiff.
    Makes use of /usr/bin/diff to do all the hard work
    Hence the name, Poor Man's colordiff (pmcolordiff)
"""

import sys
import subprocess
import re
# from colorama import Fore, Style


def main():
    ''' main driver program '''

    if len(sys.argv) < 3:
        print("Usage: {} [options] file1 file2".format(sys.argv[0]))
        print("Where file1 and file2 are files to be diffed", end="")
        print(" and options are those for diff")
        sys.exit(1)

    diffcmd = ["/usr/bin/diff"]
    diffcmd.extend(sys.argv[1:])

    try:
        proc = subprocess.run(diffcmd, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL,
                              universal_newlines=True, timeout=20)
    except subprocess.TimeoutExpired:
        print("error, timed out in executing {}".format(diffcmd))
        sys.exit(1)

    regex1 = re.compile(r'(^\d+[acd]\d+|^@@)')
    regex2 = re.compile(r'(^<|^-)')
    regex3 = re.compile(r'(^>|^\+)')

    for line in proc.stdout.split('\n'):
        for myregex, color in [(regex1, "\33[95m{}\033[00m"),  # Cyan
                               (regex2, "\033[31m{}\033[00m"), # Red
                               (regex3, "\33[32m{}\033[00m")]:  # green
            if myregex.match(line):
                print(color.format(line))
                break
        else:
            print("\033[90m{}\033[00m".format(line))


if __name__ == "__main__":
    main()
