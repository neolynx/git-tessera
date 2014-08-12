from gittle import Gittle

class MyGit:
    def __init__(self, gitdir):
        self.git = Gittle(gitdir)

    def add(self, files, message):
        self.git.commit(message=message, files=files)

    def rm(self, files, message):
        self.git.rm(files)
        self.git.commit(message=message)

    def read_author(self, tessera_path):
        author = "unknown"
        author_time = 0;
        walker = self.git.repo.get_walker(paths=[tessera_path])
        try:
            c = iter(walker).next().commit
        except StopIteration:
            print "git: author not found in %s" % tessera_path
        else:
            author = c.author
            author_time = c.author_time
        return (author, author_time)
