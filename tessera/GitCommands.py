import os
import stat
from uuid import uuid1
from subprocess import check_output, Popen
from sys import stdin, stdout, stderr

from Tessera import Tessera
from GitTessera import GitTessera
from gittle import Gittle
import shutil

class GitCommands:

    def __init__(self):
        self.gitdir = "."
        self.git = Gittle(self.gitdir)
        Tessera._tesserae = os.path.relpath("%s/.tesserae" % self.gitdir)


    def cmd_init(self, args):
        if len(args) != 0:
            stderr.write("git tessera init takes no arguments\n")
            return False

        #if self.git.is_dirty():
            #stderr.write("repo is dirty\n")
            #return False

        if os.path.exists(Tessera._tesserae):
            stderr.write("git tesserae directory already exists: %s\n"%Tessera._tesserae)
            return False
        os.mkdir(Tessera._tesserae)

        files = []
        t = "%s/template"%Tessera._tesserae
        shutil.copyfile("%s/config/template"%os.path.dirname(os.path.realpath(__file__)), t)
        files.append(t)

        t = "%s/status"%Tessera._tesserae
        shutil.copyfile("%s/config/status"%os.path.dirname(os.path.realpath(__file__)), t)
        files.append(t)

        t = "%s/types"%Tessera._tesserae
        shutil.copyfile("%s/config/types"%os.path.dirname(os.path.realpath(__file__)), t)
        files.append(t)

        self.git_add(files, "tessera: initialized")
        return True


    def cmd_ls(self, args):
        gt = GitTessera()
        tesserae = gt.ls()
        for t in tesserae:
            print t.summary()
        return True


    def cmd_show(self, args):
        if len(args) != 1:
            stderr.write("git tessera show takes identifier as argument\n")
            return False

        gt = GitTessera()
        t = gt.get( args[0] )
        if not t:
          return False

        short = t.summary()
        length = len(short)
        print "=" * length
        print short
        print "=" * length
        print t.get_body()
        return True


    def cmd_edit(self, args):
        if len(args) < 1:
            stderr.write("git tessera edit takes one or more identifier as argument\n")
            return False

        tessera_paths = []
        for key in args:
            tessera_path = None
            found = False
            for i in os.listdir(Tessera._tesserae):
                tessera_path = "%s/%s"%(Tessera._tesserae, i)
                if not stat.S_ISDIR(os.lstat(tessera_path).st_mode):
                    continue
                if i.split('-')[0] == key or i == key:
                    found = True
                    break
            if not found:
                stder.write("git tessera %s not found\n"%key)
                return False

            tessera_paths.append(tessera_path)

        tessera_files = [ "%s/tessera" % x for x in tessera_paths ]
        p = Popen( ["sensible-editor"] + tessera_files )
        p.communicate( )
        p.wait()

        #if self.git.is_dirty():
        for tessera_path in tessera_paths:
            t = Tessera(tessera_path)
            self.git_add("%s/tessera" % tessera_path, "tessera updated: %s"%t.title)
        return True

    def cmd_create(self, args):
        if len(args) < 1:
            stderr.write("git tessera create needs arguments\n")
            return False

        #if self.git.is_dirty():
        #    stderr.write("repo is dirty\n")
        #    return False

        if args:
            title = " ".join(args)
        else:
            title = "tessera title goes here"
        uuid = uuid1()
        tessera_path = "%s/%s"%(Tessera._tesserae, uuid)
        tessera_file = "%s/tessera"%tessera_path
        os.mkdir(tessera_path)
        fin = open("%s/template"%Tessera._tesserae, "r")
        fout = open(tessera_file, "w")
        for line in fin.readlines( ):
            if line == "@title@\n":
                line = "# %s\n"%title
            fout.write(line)
        fin.close()
        fout.close()

        p = Popen( ["sensible-editor", tessera_file])
        p.communicate( )
        p.wait()

        t = Tessera(tessera_path)
        self.git_add(tessera_file, "tessera created: %s"%t.title)
        return True

    def cmd_remove(self, args):
        if len(args) != 1:
            stderr.write("git tessera remove takes identifier as argument\n")
            return False

        #if self.git.is_dirty():
            #stderr.write("repo is dirty\n")
            #return False

        key = args[0]
        tessera_file = None
        tessera_path = None
        for i in os.listdir(Tessera._tesserae):
            tessera_path = "%s/%s"%(Tessera._tesserae, i)
            if not stat.S_ISDIR(os.lstat(tessera_path).st_mode):
                continue
            if i.split('-')[0] == key or i == key:
                tessera_file = "%s/tessera"%tessera_path
                break
        if not tessera_file:
            stderr.write("git tessera %s not found\n"%key)
            return False

        t = Tessera(tessera_path)
        stdout.write("remove tessera %s: %s ? [Y/n] "%(key, t.title))
        try:
            answer = stdin.readline().strip()
        except KeyboardInterrupt:
            return False
        if not answer or answer.lower() == "y":
            files = [ "%s/%s"%(tessera_path, x) for x in os.listdir(tessera_path)]
            self.git_rm(files, "tessera removed: %s"%t.title)

            from shutil import rmtree
            rmtree(tessera_path)

    def cmd_serve(self, args):
      from TesseraWeb import TesseraWeb
      web = TesseraWeb()
      web.serve()

    def git_add(self, files, message):
        stderr.write("staging %s" % files)
        self.git.commit(message=message, files=files)

    def git_rm(self, files, message):
        self.git.rm(files)
        self.git.commit(message=message)

