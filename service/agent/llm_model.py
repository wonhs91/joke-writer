from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq


# llm = ChatOllama(model='llama3.2')
llm = ChatGroq(model="llama-3.1-8b-instant")
