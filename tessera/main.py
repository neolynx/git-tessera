#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, stderr, exit

from colorful import colorful
from gitcommands import GitCommands
from exceptions import TesseraError


def main():
    cmd = "ls"
    if len(argv) > 1:
        cmd = argv[1]

    t = GitCommands()

    if hasattr(t, "cmd_%s" % cmd):
        ret = False
        try:
            ret = getattr(t, "cmd_%s" % cmd)(argv[2:])
        except TesseraError, e:
            stderr.write(colorful.bold_red("Error:") + " %s\n" % colorful.red(e))
        exit(0 if ret else 1)
    else:
        colorful.out.bold_red("unknown command: %s" % cmd)
        for cmd in dir(t):
            if cmd.startswith("cmd_"):
                colorful.out.underline(cmd[4:])
        exit(2)

if __name__ == "__main__":
    main()
