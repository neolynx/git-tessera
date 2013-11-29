#!/usr/bin/env python

from sys import argv, stdin, stdout, stderr, exit
import os
import shutil
import stat
from gittle import Gittle
from tesseracmds import TesseraCommands

from colorful import colorful

def cmp_tessera(a, b):
  aa = os.lstat("%s/tessera"%a)
  bb = os.lstat("%s/tessera"%b)
  return aa.st_mtime < bb.st_mtime

def main():
  cmd = "ls"
  if len(argv) > 1:
    cmd = argv[1]

  #try:
  t = TesseraCommands()
  #except git.exc.InvalidGitRepositoryError:
    #stderr.write("not a git repo\n")
    #exit(1)
  if hasattr(t, "cmd_%s"%cmd):
    if not getattr(t, "cmd_%s"%cmd)(argv[2:]):
      exit( 1 )
    exit( 0 )
  else:
    stderr.write("unknown command: %s\n"%cmd)
    exit(2)

if __name__ == "__main__":
    main()
