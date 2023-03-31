from config.config import Configuration
from lchainexec.lexecutor import LExecutor


class Executor:
    def __init__(self):
        self.configuration = Configuration()
        self.lexecutor = LExecutor()

    def execute(self):
        execoutput = self.lexecutor.lexec()
        print(execoutput)

if __name__ == '__main__':
    executor = Executor()
    executor.execute()