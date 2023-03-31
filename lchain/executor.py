from config.config import Configuration
from lchainexec.lexecutor import LExecutor


class Executor:
    def __init__(self):
        self.configuration = Configuration()
        self.lexecutor = LExecutor()

    def execute(self, text):
        execoutput = self.lexecutor.lexec(text)
        print(execoutput)

        return execoutput
