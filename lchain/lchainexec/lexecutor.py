from langchain import OpenAI, ConversationChain
from langchain.chains import VectorDBQAWithSourcesChain
import faiss
import pickle


class LExecutor:
    def __init__(self):
        self.temperature = 0
        self.ai_model = OpenAI(temperature=self.temperature)
        # self.chat_model = ConversationChain(llm=self.ai_model, verbose=False)
        index = faiss.read_index("resources/docs.index")
        with open("resources/faiss_store1.pkl", "rb") as f:
            store = pickle.load(f)
        store.index = index
        print(type(store))
        self.qa_chain = VectorDBQAWithSourcesChain.from_llm(llm=self.ai_model, vectorstore=store)

    def lexec(self):
        while True:
            text = input()
            if text.lower() == "bye":
                return
            result_response = self.qa_chain({"question": text})
            print(result_response['answer'])
            print(result_response['sources'])
