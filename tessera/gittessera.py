# -*- coding: utf-8 -*-

import os
import stat
from uuid import uuid1

from mygit import MyGit
from tessera import Tessera
from exceptions import ArgumentError, TesseraError


class GitTessera(object):
    SORTING = {
        "date": lambda t1, t2: t1.mtime < t2.mtime,
        "status": lambda t1, t2: cmp(t1.get_attribute("status_id"), t2.get_attribute("status_id")),
        "title": lambda t1, t2: cmp(t1.get_attribute("title").lower(), t2.get_attribute("title").lower()),
    }

    def __init__(self, config):
        self.gitdir = "."
        self.git = MyGit(self.gitdir)
        self.tesserae = os.path.join(self.gitdir, ".tesserae")
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
        return Tessera(tessera_path, self._config)

    def commit(self, t):
        """ commits a Tessera created by the create() method to the repository.
        """
        t.update()
        self.git.add(t.filename, "tessera created: %s" % t.get_attribute("title"))



