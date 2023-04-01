from config.config import Configuration
from lchainexec.lexecutor import LExecutor
import logging

class Executor:
    def __init__(self):
        self.configuration = Configuration()
        self.lexecutor = LExecutor()

    def execute(self, text):
        execoutput = self.lexecutor.lexec(text)
        logging.debug(execoutput)

        return execoutput
