from gittle import Gittle

class MyGit:
    def __init__(self, gitdir):
        self.git = Gittle(gitdir)

    def add(self, files, message):
        self.git.commit(message=message, files=files)

    def rm(self, files, message):
        self.git.rm(files)
        self.git.commit(message=message)

