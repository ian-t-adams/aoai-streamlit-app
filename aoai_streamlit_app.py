import os
import streamlit as st
import openai
from dotenv import load_dotenv  
from src.aoai_helper_funcs import generate_chat_completion, generate_completion

load_dotenv()  

openai.api_type = "azure"  
openai.api_key = os.environ['APIM_KEY']  
openai.api_base = os.environ['APIM_ENDPOINT']  
openai.api_version = os.environ['AOAI_API_VERSION']

st.title("AOAI 🤖 Chatbot")