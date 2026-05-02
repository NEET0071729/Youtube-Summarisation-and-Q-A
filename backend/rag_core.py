# rag_core.py
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_rag_chain():
    # retriever function[cite: 2]
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma(persist_directory="./data/chroma_db", embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # query re-writer for retrievel[cite: 2]
    contextual_query_system_prompt =  """You are to create a query using chat history and question. 
    The query will be a standalone question that will be used for retrieving information.
    Do not send empty question.
    """

    contextual_query_prompt = ChatPromptTemplate.from_messages([
            ("system", contextual_query_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
    ])

    # query for question and answer[cite: 2]
    query_system_prompt = """You are llm that answer question using chat history and context.
    The context is given below.
    \n\n
    {context}
    """
    query_prompt = ChatPromptTemplate.from_messages([
        ("system", query_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature= 0)
    llm2 = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-lite", temperature= 0)
    # retrieving using remade query stage[cite: 2]
    rephrase_chain = contextual_query_prompt | llm2 | StrOutputParser()

    # formatting retrieved docs[cite: 2]
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def context_retriever(input_dict):
        if input_dict.get("chat_history"):
            rephrased = rephrase_chain.invoke({
                "input": input_dict["input"],
                "chat_history": input_dict["chat_history"]
            })
            print(f"[DEBUG] Rephrased query: {repr(rephrased)}")
            # Fall back to original input if rephrase returned empty
            return rephrased.strip() if rephrased and rephrased.strip() else input_dict["input"]
        else:
            return input_dict["input"]
        
    rag_chain = (
        RunnablePassthrough.assign(
            context = context_retriever | retriever | format_docs
        )
        | query_prompt
        | llm
        | StrOutputParser()
    )

    # Return just the chain, let FastAPI handle the invocations
    return rag_chain