from langchain.prompts import ChatPromptTemplate
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain.chains import ConversationalRetrievalChain
# from backend.vector_handler import VectorHandler


BASE_LLM_URL = "http://host.docker.internal:11434"

prompt_template = ChatPromptTemplate.from_messages([
    ("system",
    "You are an expertise in computer networking and internet with immense experience,"\
        "excellent troubleshooter and design expert"),
    ("human",
    "Answer the question based on the following context in "\
        "a most accurate way:\n{context}\n\nQuestion: {question}")
])

class NetMate:

    def __init__(self, model="mistral"):

        self.llm_url = BASE_LLM_URL
        self.model_name = model
        self.llm = ChatOllama(model=self.model_name, base_url=self.llm_url)
        # self.vh = VectorHandler()

    def create_conversational_chain(self, vh):
        """Create the Conversational Retrieval Chain."""

        conversational_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vh.vector_store.as_retriever(),
            combine_docs_chain_kwargs={"prompt": prompt_template}
        )
        return conversational_chain


    def query(self, question, chat_history, chain):
        
        return chain.invoke({"question": question, "chat_history": chat_history})
