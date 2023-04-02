"""This is the logic for ingesting custom confluence documents into LangChain."""

from langchain.text_splitter import CharacterTextSplitter
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle
import os


class DocIndexer:
    def __init__(self, conf):
        space = conf.user_conf["input_options"]["space"]
        self.chunk_size = conf.user_conf["model_tuning"]["llm_context_character_len"]
        self.seperator = conf.user_conf["model_tuning"]["llm_context_sep"]
        self.basepath = f"{os.getcwd()}/resources/pickle_files/{space}"

    def run(self, input_files):
        data = []
        sources = []
        for p in input_files:
            with open(p) as f:
                data.append(f.read())
            sources.append(p)
        if not os.path.exists(self.basepath):
            os.makedirs(self.basepath)
        # Here we split the documents, as needed, into smaller chunks.
        # We do this due to the context limits of the LLMs.
        text_splitter = CharacterTextSplitter(chunk_size=self.chunk_size, separator=self.seperator)
        docs = []
        metadatas = []
        for i, d in enumerate(data):
            splits = text_splitter.split_text(d)
            if len(docs) < 58:
                docs.extend(splits)
                metadatas.extend([{"source": sources[i]}] * len(splits))
            else:
                break

        # Here we create a vector store from the documents and save it to disk.
        store = FAISS.from_texts(docs, OpenAIEmbeddings(), metadatas=metadatas)
        faiss.write_index(store.index, f"{self.basepath}/{self.space}.index")
        store.index = None
        with open(f"{self.basepath}/{self.space}.pkl", "wb") as f:
            pickle.dump(store, f)
