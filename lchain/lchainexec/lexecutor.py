import os

from langchain import OpenAI
from langchain.chains import VectorDBQAWithSourcesChain
import logging
import faiss
import pickle
from lchain.config.config import Config


class LExecutor:
    def __init__(self):
        conf = Config()
        base_path = "training_components/resources/pickle_files"
        space = conf.user_conf["input_options"]["space"]
        pickle_file_path = f"{os.getcwd()}/{base_path}/{space}/{space}.pkl"
        index_file_path = f"{os.getcwd()}/{base_path}/{space}/{space}.index"
        self.temperature = conf.user_conf["model_tuning"]["llm_temperature"]
        self.ai_model = OpenAI(temperature=self.temperature)
        index = faiss.read_index(index_file_path)
        with open(pickle_file_path, "rb") as f:
            store = pickle.load(f)
        store.index = index
        logging.debug(type(store))
        self.qa_chain = VectorDBQAWithSourcesChain.from_llm(
            llm=self.ai_model, vectorstore=store)

    def lexec(self, text):
        result_response = self.qa_chain({"question": text})
        logging.debug(result_response['answer'])
        logging.debug(result_response['sources'])

        return result_response['answer']
