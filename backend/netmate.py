from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama

# from langchain.chains import ConversationalRetrievalChain
# from backend.vector_handler import VectorHandler


BASE_LLM_URL = "http://host.docker.internal:11434"

prompt_template = ChatPromptTemplate.from_messages([
    ("system",
    "You are an expertise in computer networking and internet with immense experience,"\
    "there might a chat history as well present here in case,"\
    "you are an excellent troubleshooter and design expert in "\
    "the field of computer networking and internet. "\
    "Use the retrieved context to answer the question in a detailed manner."\
    "\n Context: {context}"),
    MessagesPlaceholder("chat_history"),
    ("human","Question: {input}")
])

contextualize_q_system_prompt = (
    "A chat history may or may not be present but given the the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, just "
    "reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

class NetMate:

    def __init__(self, model="mistral"):

        self.llm_url = BASE_LLM_URL
        self.model_name = model
        self.llm = ChatOllama(model=self.model_name, base_url=self.llm_url)
        # self.vh = VectorHandler()

    # old implemetation
    '''
    def create_conversational_chain(self, vh):
        """Create the Conversational Retrieval Chain."""

        conversational_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vh.vector_store.as_retriever(),
            combine_docs_chain_kwargs={"prompt": prompt_template}
        )
        return conversational_chain
    '''

    def create_conversational_chain(self, vh):
        """Create the Conversational Retrieval Chain."""

        retriever = vh.vector_store.as_retriever()
        history_aware_retriever = create_history_aware_retriever(
            self.llm,
            retriever,
            contextualize_q_prompt
        )
        question_answer_chain = create_stuff_documents_chain(
            self.llm,
            prompt_template
        )

        rag_chain = create_retrieval_chain(
            history_aware_retriever,
            question_answer_chain
        )

        return rag_chain

    def query(self, question, chat_history, chain):
        return chain.invoke({"input": question, "chat_history": chat_history})
