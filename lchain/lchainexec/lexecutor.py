from langchain import OpenAI, ConversationChain

class LExecutor:
    def __init__(self):
        self.temperature = 0
        self.ai_model = OpenAI(temperature=self.temperature)
        self.chat_model = ConversationChain(llm=self.ai_model, verbose=False)


    def lexec(self):
        while True:
            text = input()
            if text.lower() == "bye":
                return
            print(self.chat_model.predict(input=text))
