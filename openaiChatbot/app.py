import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]= "true"
os.environ["LANGCHAIN_PROJECT"]="QnA chatbot with open AI"

prompt= ChatPromptTemplate.from_messages([
    ("system","As an expert AI Software Engineer answer the question"),
    ("user","Question:{question}")
])

def generate_response(question, api_key, llm, temperature, max_tokens):
    openai.api_key=api_key
    os.environ["OPENAI_API_KEY"] = api_key
    llm= ChatOpenAI(model=llm)
    output_parser= StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer


st.sidebar.title("Settings")
api_key_input= st.sidebar.text_input("Enter you Open API Key:", type="password") 

engine=st.sidebar.selectbox("Select an OPENAI Model", ["gpt-4o","gpt-4-turbo","gtp-4"])

temperature= st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.5)
max_tokens=st.sidebar.slider("MAX Tokens",min_value=50, max_value=300, value=100)

st.write("Ask a queastion")
user_input=st.text_input("Question:")

if user_input:
    response= generate_response(user_input,api_key_input,engine,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please ask question")