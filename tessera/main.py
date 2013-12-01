#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, stderr, exit
from gitcommands import GitCommands


def main():
    cmd = "ls"
    if len(argv) > 1:
        cmd = argv[1]

    #try:
    t = GitCommands()
    #except git.exc.InvalidGitRepositoryError:
        #stderr.write("not a git repo\n")
        #exit(1)
    if hasattr(t, "cmd_%s" % cmd):
        if not getattr(t, "cmd_%s" % cmd)(argv[2:]):
            exit(1)
        exit(0)
    else:
        stderr.write("unknown command: %s\n" % cmd)
        exit(2)

if __name__ == "__main__":
    main()
