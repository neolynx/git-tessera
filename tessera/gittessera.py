# -*- coding: utf-8 -*-

import os
import stat
from uuid import uuid1

from mygit import MyGit
from tessera import Tessera
from exceptions import ArgumentError, TesseraError
from dulwich.config import StackedConfig
from time import time

def cmp_status( t1, t2 ):
    s1 = t1.get_attribute("status_id")
    s2 = t2.get_attribute("status_id")
    if s1 != s2:
        return cmp( s1, s2 )
    return cmp( t2.get_attribute("updated"), t1.get_attribute("updated"))


class GitTessera(object):
    SORTING = {
        "date": lambda t1, t2: t1.mtime < t2.mtime,
        "status": cmp_status,
        "title": lambda t1, t2: cmp(t1.get_attribute("title").lower(), t2.get_attribute("title").lower()),
    }

    def __init__(self, config):
        self.gitdir = "."
        self.git = MyGit(self.gitdir)
        if self.gitdir != ".":
           self.tesserae = os.path.join(self.gitdir, ".tesserae")
        else:
           self.tesserae = ".tesserae"
        self._config = config

    def ls(self, args=[]):
        if not os.path.exists(self.tesserae):
            return False

        try:
            idx = args.index("--sort")
            sortfunc = GitTessera.SORTING[args[idx + 1]]
        except ValueError:
            sortfunc = GitTessera.SORTING["status"]
        except IndexError:
            raise ArgumentError("Please specify a sort algorithm. Available: %s" % (", ".join(GitTessera.SORTING.keys())))
        except KeyError:
            raise ArgumentError("No sort algorithm for '%s' available" % args[idx + 1])

        try:
            idx = args.index("--tags")
            tags = args[idx + 1].split(",")
        except ValueError:
            tags = None
        except IndexError:
            raise ArgumentError("Please specify minimum one tag.")

        contents = [self.tesserae + "/" + x for x in os.listdir(self.tesserae) if stat.S_ISDIR(os.lstat(self.tesserae + "/" + x).st_mode)]
        tesserae = []
        for tessera_path in contents:
            t = Tessera(tessera_path, self._config)

            if t.get_attribute("updated") == 0:
                tessera_info = "%s/info" % tessera_path
                fout = open(tessera_info, "w")
                author, author_time = self.git.read_author(tessera_path)
                import re
                r = re.compile("^([^\<]+) \<([^\>]+)\>$")
                m = r.search( author )
                if m:
                    fout.write("author: %s\n" % m.group(1))
                    fout.write("email: %s\n" % m.group(2))
                    fout.write("updated: %d\n"%author_time)
                fout.close()


            te_tags = t.get_attribute("tags")
            if not tags or any(x in te_tags for x in tags):
                tesserae.append(t)

        tesserae = sorted(tesserae, cmp=sortfunc)
        return tesserae

    def get(self, key):
        for i in os.listdir(self.tesserae):
            tessera_path = os.path.join(self.tesserae, i)
            if not stat.S_ISDIR(os.lstat(tessera_path).st_mode):
                continue
            if i.split('-')[0] == key or i == key:
                break
        if not tessera_path:
            raise TesseraError("git tessera %s not found" % key)
        return Tessera(tessera_path, self._config)

    def create(self, title="tessera title goes here"):
        """ create a new tessera with title {title}.

            @returns Tessera object of the new Tessera
        """
        uuid = uuid1()
        tessera_path = os.path.join(Tessera._tesserae, str(uuid))
        tessera_file = "%s/tessera" % tessera_path
        os.mkdir(tessera_path)
        fin = open(os.path.join(Tessera._tesserae, "template"), "r")
        fout = open(tessera_file, "w")
        for line in fin.readlines():
            if line == "@title@\n":
                line = "# %s\n" % title
            fout.write(line)
        fin.close()
        fout.close()

        tessera_info = "%s/info" % tessera_path
        fout = open(tessera_info, "w")
        c = StackedConfig(StackedConfig.default_backends())
        fout.write("author: %s\n"%c.get("user", "name"))
        fout.write("email: %s\n"%c.get("user", "email"))
        fout.write("updated: %d\n"%int(time()))
        fout.close()

        return Tessera(tessera_path, self._config)

    def commit(self, t):
        """ commits a Tessera created by the create() method to the repository.
        """
        files = [ os.path.join(t.tessera_path, "tessera"), os.path.join(t.tessera_path, "info") ]
        self.git.add(files, "tessera created: %s" % t.get_attribute("title"))



