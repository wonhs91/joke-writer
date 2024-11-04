from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq


# llm = ChatOllama(model='llama3.2')
llm = ChatGroq(model="gemma2-9b-it")
