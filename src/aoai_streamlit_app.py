'''
Using the https://github.com/kirkhofer/data-ai/blob/main/aoai/chatbot.py repo from Kirk Hofer as a starting point.
'''

import os
import openai
import streamlit as st
from dotenv import load_dotenv  
import aoai_helpers as helpers

load_dotenv()  

openai.api_type = "azure"  
openai.api_key = os.environ['APIM_KEY']  
openai.api_base = os.environ['APIM_ENDPOINT']  
openai.api_version = os.environ['AOAI_API_VERSION']

# Preload environment variables and sidebar settings
helpers.load_settings(reload_api_settings=True)

# Create containers for the header, chat window, and footer - will use sidebar for setting model parameters
header_container = st.container()
chat_container = st.container()
footer_container = st.container()

# Top level title and description of the app
with header_container:
    st.title("Interact with an Azure OpenAI 🤖", anchor="top", help='''This demo showcases the Azure OpenAI Service, Azure API Management Service,
          and Azure Web Apps with Streamlit.''')

# Pull up the messages if they exist - needed
if 'messages' not in st.session_state:
    helpers.env_to_st_session_state('SYSTEM','system', "You are an AI assistant that helps people.")
    st.session_state.messages = []
    st.session_state.messages.append({"role":"system","content":st.session_state.system})


with st.sidebar.title("Model Parameters", anchor="top", help='''The model parameters are used to control the behavior of the model. 
                      Each parameter has its own tooltip.'''):
    # if st.session_state['show_settings']:  

    # Create a dictionary containing the available models for each completion type 
    # ###UPDATE 07/12/2023 first round will only accomodate the Chat models until gpt-35-turbo-instruct is released
    available_models = {  
        "Chat": ["gpt-4", "gpt-4-32k", "gpt-35-turbo", "gpt-35-turbo-16k"],  
        #"Completion": ["text-davinci-003"],  
        #"Embedding": ["text-embedding-ada-002"]  
    }
    # These next few lines are unnecessary until other completion types are added
    # callEndpoints = ["Chat", "Completion"]#, "Embedding"]  
    # completion_type = st.sidebar.radio(  
    #     "Choose whether you wish to engage in a Chat (ChatCompletions) or Completions interaction:",# for text or Embeddings for a demonstration of embeddings outputs:",  
    #     callEndpoints, key="completionkey", help='''Chat Experience will utilize the GPT-35-Turbo and GPT-4 models to engage in a chat-like conversation. Completion will allow
    #     for a single prompt and then response and only works with older model types. Embeddings will provide a response demonstrating what an embedding translation looks like.''')
    # Update the model_options depending on the selected completion type  
    # model_options = available_models[completion_type]

    # ###UPDATE model_options hard-coded to Chat for now 07/12/2023
    model_options = available_models["Chat"]

    # Set a default value for the model
    default_index = model_options.index("gpt-35-turbo-16k")

    # model_options
    model = st.sidebar.selectbox("Choose a model:", model_options, key="modelkey", index=default_index,
                                help='''Choose the model with which you wish to interact. Defaults to gpt-35-turbo-16k.
                                You can select the original GPT-35-Turbo (ChatGPT) model with 4k or 16k token contexts.
                                The GPT-4 models with 8k or 32k token contexts are also available.''')

    # Then, when a model is selected, load the parameters for that model
    if model is not None:
        params = helpers.model_params[model]
    else:
        params = helpers.model_params["gpt-35-turbo-16k"]
    # Create a system message box so users may supply their own system message
    st.sidebar.text_area("System Message", value=st.session_state.system, height=150, key="txtSystem", help='''Enter a system message here. This is where you define the personality, rules of behavior, and guardrails for your Assistant.''')
    # Read in the appropriate model specific parameters for the streamlit sliders - these all come from the dictionary in aoai_helpers.py
    # These are passed into the appropriate helpers.generate_ function calls
    # Default values are set with value= and are not defined in the dictionary
    temperature = st.sidebar.slider(label="Set a temperature:", min_value=params['temp_min'], max_value=params['temp_max'], value=st.session_state.temperature,
                                    step=params["temp_step"], help=params['temp_help'], key="tempkey")
    max_tokens = st.sidebar.slider(label="Set max_tokens:", min_value=params['tokens_min'], max_value=params['tokens_max'], value=st.session_state.maxtokens,
                                step=params["tokens_step"], help=params['tokens_help'], key="tokenskey")
    top_p = st.sidebar.slider(label="Set top_p:", min_value=params['top_p_min'], max_value=params['top_p_max'], value=st.session_state.topp,
                            step=params["top_p_step"], help=params['top_p_help'], key="top_pkey")
    frequency_penalty = st.sidebar.slider(label="Set frequency_penalty:", min_value=params['frequency_penalty_min'], max_value=params['frequency_penalty_max'], value=st.session_state.frequencypenalty,
                                        step=params["frequency_penalty_step"], help=params['frequency_penalty_help'], key="frequency_penaltykey") 
    presence_penalty = st.sidebar.slider(label="Set presence_penalty:", min_value=params['presence_penalty_min'], max_value=params['presence_penalty_max'], value=st.session_state.presencepenalty,
                                        step=params["presence_penalty_step"], help=params['presence_penalty_help'], key="presence_penaltykey")

    # Save the chosen parameters to the system state upon submission
    st.sidebar.button("Save Model Parameter Settings",
                on_click=helpers.save_session_state(),
                key="saveButton",
                help='''Save the model parameter settings to the session state.''',
                type="secondary")
    
    # st.sidebar.success('Settings saved successfully!', icon="✅")

with chat_container:
    if st.session_state['messages']:
        for message in st.session_state.messages:
            if message["role"] != "system":  # Skip system message
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])  

    if prompt := st.chat_input("💬 Window - Go ahead and type!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            for response in helpers.generate_chat_completion(engine=st.session_state.engine,
                                                            messages=[
                                                                {"role": m["role"], "content": m["content"]}
                                                                for m in st.session_state.messages
                                                            ],
                                                            temperature=st.session_state.temperature,
                                                            max_tokens=st.session_state.maxtokens,
                                                            top_p=st.session_state.topp,
                                                            frequency_penalty=st.session_state.frequencypenalty,
                                                            presence_penalty=st.session_state.presencepenalty,
                                                            stop=None,
                                                            stream=True):

                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with footer_container:
    st.button("Clear All Settings and Chat History",
          on_click=lambda: st.session_state.clear(),
          type="primary",
          help='''Clear all settings and chat history from the session state.''')
    st.caption(":red[NOTE: ALL SYSTEM MESSAGES, PROMPTS, AND COMPLETIONS ARE LOGGED FOR THIS DEMO.]")
    st.caption(f":red[DO NOT ENTER ANY SENSITIVE INFORMATION.]")

# # Path: aoai-streamlit-app\src\aoai_streamlit_app.py

# ###UPDATE 07/16/2023 - Add in ability to pass parameters for apim endpoint, key, and aoai_version
# '''
# import argparse
# import os
# import streamlit as st

# # Define the command line arguments
# parser = argparse.ArgumentParser()
# parser.add_argument('--apim-endpoint', type=str, required=True, help='The Azure OpenAI API Management endpoint')
# parser.add_argument('--apim-key', type=str, required=True, help='The Azure OpenAI API Management key')
# args = parser.parse_args()

# # Set the environment variables
# os.environ['APIM_ENDPOINT'] = args.apim_endpoint
# os.environ['APIM_KEY'] = args.apim_key

# # Define the Streamlit app
# def main():
#     # Your Streamlit app code here
#     pass

# if __name__ == '__main__':
#     main()
# '''