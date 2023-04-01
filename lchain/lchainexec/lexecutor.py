from langchain import OpenAI, ConversationChain
from langchain.chains import VectorDBQAWithSourcesChain
import logging
import faiss
import pickle


class LExecutor:
    def __init__(self):
        self.temperature = 0
        self.ai_model = OpenAI(temperature=self.temperature)
        # self.chat_model = ConversationChain(llm=self.ai_model, verbose=False)
        index = faiss.read_index("lchain/resources/readme.index")
        with open("lchain/resources/readme.pkl", "rb") as f:
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
