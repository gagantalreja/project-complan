from langchain.llms import OpenAI

class LExecutor:
    def __init__(self):
        self.temperature = 0.3
        self.ai_model = OpenAI(temperature=self.temperature)

    def lexec(self):
        text = "What is a good name for tech company to power healthcare data?"
        return self.ai_model(text)
