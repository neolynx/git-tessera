import os
import stat

from gittle import Gittle
from tessera import Tessera

class GitTessera(object):

    def __init__(self):
        self.gitdir = "."
        self.git = Gittle(self.gitdir)
        self.tesserae = "%s/.tesserae"  % self.gitdir

    def ls(self, args = []):
        # FIXME: check args
        if not os.path.exists(self.tesserae):
            return False

        contents = [ self.tesserae + "/" + x for x in os.listdir(self.tesserae) if stat.S_ISDIR(os.lstat(self.tesserae + "/" + x).st_mode)]
        tesserae = []
        for tessera_path in contents:
            tesserae.append(Tessera(tessera_path))
        tesserae.sort( key = lambda x: x.status_id )
        return tesserae

