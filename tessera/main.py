#!/usr/bin/env python

from sys import argv, stdin, stdout, stderr, exit
from subprocess import check_output, Popen
import shutil
import re
from gittle import Gittle
from gittessera import GitTessera
from uuid import uuid1

from colorful import colorful

def main():
  cmd = "ls"
  if len(argv) > 1:
    cmd = argv[1]

  #try:
  t = GitTessera()
  #except git.exc.InvalidGitRepositoryError:
    #stderr.write("not a git repo\n")
    #exit(1)
  if hasattr(t, cmd):
    if not getattr(t, cmd)(argv[2:]):
      exit( 1 )
    exit( 0 )
  else:
    stderr.write("unknown command: %s\n"%cmd)
    exit(2)

if __name__ == "__main__":
    main()
