import os  
import openai  
import streamlit as st  
from dotenv import load_dotenv  
  
load_dotenv() 

with st.sidebar:
    openai.api_type = "azure"  
    openai.api_key = os.environ['APIM_KEY']
    openai_api_key = os.environ['APIM_KEY']  
    openai.api_base = os.environ['APIM_ENDPOINT']  
    openai.api_version = os.environ['AOAI_API_VERSION']  

st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(engine="gpt-4-32k", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)