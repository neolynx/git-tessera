from gittle import Gittle

class Tessera:
    _tesserae = None
    _status = []

    def __init__(self, tessera_path):
        self.tessera_path = tessera_path
        self.filename = "%s/tessera" % tessera_path
        self.title = None
        self.status = None
        self._read()
        self._parse()

        if Tessera._status:
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

    def _read(self):
        if not os.path.exists(self.filename):
            stderr.write("tessera file not found: %s\n"%self.fielname)
            return None

        f = open(self.filename, 'r')
        self.body = f.read().split('\n')
        f.close()

    def _parse(self):
        self.title = "no title"
        for i in range(len(self.body)):
            if self.body[i].startswith("# "):
                self.title = self.body[i][2:].strip()
                self.body.pop(i)
                break

        self.status = "no status"
        for i in range(len(self.body)):
            if self.body[i].startswith("@status "):
                self.status = self.body[i][8:].strip()
                self.body.pop(i)
                break

    def summary(self):
        l = len(self.title)
        color = None
        for s in Tessera._status:
            if s[0] == self.status:
                color = s[1]
                break
        status = self.status
        if color:
            if hasattr(colorful, color):
                f = getattr(colorful, color)
                status = f(self.status)
                return "%s %s %s %s"%(self.get_ident_short(), colorful.bold_white(self.title), " " * (40 - l), status)

    def get_ident(self ):
        return os.path.basename(self.tessera_path)

    def get_ident_short(self):
        return self.get_ident().split('-')[0]

    def get_body(self):
        return '\n'.join(self.body)
