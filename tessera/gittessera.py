import os
import stat

from gittle import Gittle
from te import Tessera

class GitTessera:

    def __init__(self):
        self.gitdir = "."
        self.git = Gittle(self.gitdir)
        self.tesserae = "%s/.tesserae"  % self.gitdir

    def ls(self, args = []):
        # FIXME: check args
        if not os.path.exists(self.tesserae):
            return False

        contents = [ self.tesserae + "/" + x for x in os.listdir(self.tesserae) if stat.S_ISDIR(os.lstat(self.tesserae + "/" + x).st_mode)]
        sorted(contents, cmp = _cmp_tessera)
        tesserae = []
        for tessera_path in contents:
            tesserae.append(Tessera(tessera_path))
        return tesserae

def _cmp_tessera(a, b):
  aa = os.lstat("%s/tessera"%a)
  bb = os.lstat("%s/tessera"%b)
  return aa.st_mtime < bb.st_mtime


