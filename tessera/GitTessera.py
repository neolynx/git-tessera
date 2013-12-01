import os
import stat

from gittle import Gittle
from Tessera import Tessera

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
        tesserae = []
        for tessera_path in contents:
            tesserae.append(Tessera(tessera_path))
        tesserae.sort( key = lambda x: x.status_id )
        return tesserae

    def get(self, key):
        tessera_file = None
        for i in os.listdir(self.tesserae):
            tessera_path = "%s/%s"%(self.tesserae, i)
            if not stat.S_ISDIR(os.lstat(tessera_path).st_mode):
                continue
            if i.split('-')[0] == key or i == key:
                break
        if not tessera_path:
            stderr.write("git tessera %s not found\n"%key)
            return None
        return Tessera(tessera_path)

