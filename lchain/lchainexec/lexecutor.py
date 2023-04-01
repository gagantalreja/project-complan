from langchain import OpenAI, ConversationChain
from langchain.chains import VectorDBQAWithSourcesChain
from langchain.prompts import PromptTemplate
import logging
import faiss
import pickle


class LExecutor:
    def __init__(self):
        self.temperature = 0
        self.ai_model = OpenAI(temperature=self.temperature)
        # self.chat_model = ConversationChain(llm=self.ai_model, verbose=False)
        index = faiss.read_index("lchain/resources/inno_doc3.index")
        with open("lchain/resources/inno_doc3.pkl", "rb") as f:
            store = pickle.load(f)
        store.index = index
        logging.debug(type(store))
        combine_prompt_template = """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
        If you don't know the answer, just say that you don't know. Don't try to make up an answer.
        ALWAYS return a "SOURCES" part in your answer.

        QUESTION: Hi?
        =========
        Content: Hello!, I'm AMA bot, you can ask me questions relevant to documentation.
        Source: 28-pl
        Content: I don't know.
        Source: 30-pl
        Content: EMPI is a Innovaccer generated unique ID assigned to a patient.
        Source: 4-pl
        =========
        FINAL ANSWER: Hello!, I'm AMA bot, you can ask me questions relevant to documentation.
        SOURCES: 28-pl

        QUESTION: What is DAP?
        =========
        Content: Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.  \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world. \n\nGroups of citizens blocking tanks with their bodies. Everyone from students to retirees teachers turned soldiers defending their homeland.
        Source: 0-pl
        Content: And we won’t stop. \n\nWe have lost so much to COVID-19. Time with one another. And worst of all, so much loss of life. \n\nLet’s use this moment to reset. Let’s stop looking at COVID-19 as a partisan dividing line and see it for what it is: A God-awful disease.  \n\nLet’s stop seeing each other as enemies, and start seeing each other for who we really are: Fellow Americans.  \n\nWe can’t change how divided we’ve been. But we can change how we move forward—on COVID-19 and other issues we must face together. \n\nI recently visited the New York City Police Department days after the funerals of Officer Wilbert Mora and his partner, Officer Jason Rivera. \n\nThey were responding to a 9-1-1 call when a man shot and killed them with a stolen gun. \n\nOfficer Mora was 27 years old. \n\nOfficer Rivera was 22. \n\nBoth Dominican Americans who’d grown up on the same streets they later chose to patrol as police officers. \n\nI spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves.
        Source: 24-pl
        Content: And a proud Ukrainian people, who have known 30 years  of independence, have repeatedly shown that they will not tolerate anyone who tries to take their country backwards.  \n\nTo all Americans, I will be honest with you, as I’ve always promised. A Russian dictator, invading a foreign country, has costs around the world. \n\nAnd I’m taking robust action to make sure the pain of our sanctions  is targeted at Russia’s economy. And I will use every tool at our disposal to protect American businesses and consumers. \n\nTonight, I can announce that the United States has worked with 30 other countries to release 60 Million barrels of oil from reserves around the world.  \n\nAmerica will lead that effort, releasing 30 Million barrels from our own Strategic Petroleum Reserve. And we stand ready to do more if necessary, unified with our allies.  \n\nThese steps will help blunt gas prices here at home. And I know the news about what’s happening can seem alarming. \n\nBut I want you to know that we are going to be okay.
        Source: 5-pl
        Content: DAP stands for Data Activation Platform. DAP helps user to integrate healthcare data into Innovaccer Data Model.
        Source: 34-pl
        =========
        FINAL ANSWER: DAP stands for Data Activation Platform
        SOURCES: 34-pl

        QUESTION: {question}
        =========
        {summaries}
        =========
        FINAL ANSWER:"""
        self.combine_prompt = PromptTemplate(
            template=combine_prompt_template, input_variables=["summaries", "question"]
        )
        self.qa_chain = VectorDBQAWithSourcesChain.from_llm(
            llm=self.ai_model, vectorstore=store
        )
        # self.qa_chain = VectorDBQAWithSourcesChain.from_llm(
        #     llm=self.ai_model, vectorstore=store, combine_prompt=self.combine_prompt
        # )

    def lexec(self, text):
        result_response = self.qa_chain({"question": text})
        logging.debug(result_response["answer"])
        logging.debug(result_response["sources"])

        return result_response["answer"]
