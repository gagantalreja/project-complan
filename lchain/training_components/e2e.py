"""
For model tuning :
update the source documents under user_config.json file
and run this module for which converts confluence pages to markdown, then generate pickle files
which can be served to LLMs for reponses
Note - to directly run it, change your current directory to its directory
"""

from lchain.config.config import Config
from lchain.training_components.confluence_to_md import MarkDownExe
from lchain.training_components.indexer import DocIndexer


class ModelTuner:

    def __init__(self):
        config = Config()
        self.markdown_exe = MarkDownExe(config)
        self.indexer = DocIndexer(config)

    def run(self):
        structured_dataset = self.markdown_exe.get_dataset()
        self.indexer.run(structured_dataset)


if __name__ == "__main__":
    ModelTuner().run()
