import os
import re

from gittle import Gittle
from colorful import colorful

class Tessera:
    _tesserae = None
    _status = []
    _te_types = []

    def __init__(self, tessera_path):
        self.tessera_path = tessera_path
        self.filename = "%s/tessera" % tessera_path
        self.title = None
        self.status = None
        self.te_type = None
        self._read()
        self._parse()

        if self._status:
            return

        status_file = "%s/status" % Tessera._tesserae
        if not os.path.exists(status_file):
            Tessera._status = False
            return

        f = open(status_file, 'r')
        for line in f.readlines():
            line = line.strip()
            if line:
                a = re.split(r'[ \t]+', line)
                if len(a) != 2:
                    print "invalid status line: %s"%line
                    break
                Tessera._status.append( ( a[0], a[1] ) )
        f.close()

        if self._te_types:
            return

        types_file = "%s/types" % Tessera._tesserae
        if not os.path.exists(types_file):
            Tessera._te_types = False
            return

        f = open(types_file, 'r')
        for line in f.readlines():
            line = line.strip()
            if line:
                a = re.split(r'[ \t]+', line)
                if len(a) != 2:
                    print "invalid te_types line: %s"%line
                    break
                Tessera._te_types.append( ( a[0], a[1] ) )
        f.close()


    def _read(self):
        if not os.path.exists(self.filename):
            stderr.write("tessera file not found: %s\n"%self.fielname)
            return None

        f = open(self.filename, 'r')
        self.body = f.read().split('\n')
        f.close()

    def _parse(self):
        self.title = None
        self.status = None
        count = range(len(self.body))
        i = 0
        while i < len(self.body):
            if self.body[i].startswith("# "):
                self.title = self.body[i][2:].strip()
                self.body.pop(i)
            elif self.body[i].startswith("@status "):
                self.status = self.body[i][8:].strip()
                self.body.pop(i)
            elif self.body[i].startswith("@type "):
                self.te_type = self.body[i][6:].strip()
                self.body.pop(i)
            else:
                i += 1

            if self.title and self.status and self.te_type:
              break
            count = range(len(self.body))

        if not self.title:
          self.title = "no title"
        if not self.status:
          self.status = "no status"
        if not self.te_type:
          self.te_type = "no te_type"

    def summary(self):
        len_title = len(self.title)
        len_status = len(self.status)
        title = self.title
        color = None
        if Tessera._status:
            for s in Tessera._status:
                if s[0] == self.status:
                    color = s[1]
                    break
            status = self.status
        else:
            status = "no status available"
        if color:
            if hasattr(colorful, color):
                f = getattr(colorful, color)
                status = f(self.status)

        color = None
        if Tessera._te_types:
            for s in Tessera._te_types:
                if s[0] == self.te_type:
                    color = s[1]
                    break
            te_type = self.te_type
        else:
            te_type = "no type available"
        if color:
            if hasattr(colorful, color):
                f = getattr(colorful, color)
                title = f(title)

        return "%s %s %s %s %s %s"%(self.get_ident_short(), title, " " * (40 - len_title), status, " " * (10 - len_status), te_type)

    def ident(self):
        return dict(ident=self.get_ident(), title=self.title, filename=self.filename, body=self.get_body())


    def get_ident(self ):
        return os.path.basename(self.tessera_path)

    def get_ident_short(self):
        return self.get_ident().split('-')[0]

    def get_body(self):
        return '\n'.join(self.body)
