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


# Pre-load environment variables to point to our API-M endpoint and key from our .env file
helpers.load_setting('AOAI_API_TYPE','apitype','azure')
helpers.load_setting('AOAI_API_VERSION','apiversion','2023-05-15')
helpers.load_setting('APIM_KEY','apikey','')
helpers.load_setting('APIM_ENDPOINT','apiendpoint','')
# Load in some Streamlit sidebar settings
helpers.load_setting('ST_ENGINE','engine','gpt-35-turbo-16k')
helpers.load_setting('ST_TEMPERATURE', 'temperature', 0.5)
helpers.load_setting('ST_MAX_TOKENS', 'maxtokens', 800)
helpers.load_setting('ST_TOP_P', 'topp', 0.90)
helpers.load_setting('ST_FREQUENCY_PENALTY', 'frequencypenalty', 0.0)
helpers.load_setting('ST_PRESENCE_PENALTY', 'presencepenalty', 0.0)

st.title("Interact with a 🤖")

# Turn on the settings sidebar by default
if 'show_settings' not in st.session_state:  
    st.session_state.show_settings = True 

# Pull up the messages if they exist
if 'messages' not in st.session_state:
    helpers.load_setting('SYSTEM','system', "Please insert your system message to define your Assistant.")
    st.session_state.messages = []
    st.session_state.messages.append({"role":"system","content":st.session_state.system})


with st.sidebar:
    st.button("Settings",on_click=helpers.toggle_settings)
    if st.session_state['show_settings']:  
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
        default_index = model_options.index("gpt-35-turbo")

        # model_options
        model = st.selectbox("Choose a model:", model_options, key="modelkey", index=default_index,
                                    help='''Choose the model with which you wish to interact.''')

        # Then, when a model is selected, load the parameters for that model
        if model is not None:
            params = helpers.model_params[model]
        else:
            params = helpers.model_params["gpt-35-turbo"]

        with st.form("AOAI_Model_Parameters"):
            # Create a system message box so users may supply their own system message
            st.text_area("System Message", value=st.session_state.system,height=100,key="txtSystem")
            # Read in the appropriate model specific parameters for the streamlit sliders - these all come from the dictionary in aoai_helpers.py
            # These are passed into the appropriate helpers.generate_ function calls
            # Default values are set with value= and are not defined in the dictionary
            temperature = st.slider(label="Set a temperature:", min_value=params['temp_min'], max_value=params['temp_max'], value=st.session_state.temperature,
                                            step=params["temp_step"], help=params['temp_help'], key="tempkey")
            max_tokens = st.slider(label="Set max_tokens:", min_value=params['tokens_min'], max_value=params['tokens_max'], value=st.session_state.maxtokens,
                                        step=params["tokens_step"], help=params['tokens_help'], key="tokenskey")
            top_p = st.slider(label="Set top_p:", min_value=params['top_p_min'], max_value=params['top_p_max'], value=st.session_state.topp,
                                    step=params["top_p_step"], help=params['top_p_help'], key="top_pkey")
            frequency_penalty = st.slider(label="Set frequency_penalty:", min_value=params['frequency_penalty_min'], max_value=params['frequency_penalty_max'], value=st.session_state.frequencypenalty,
                                                step=params["frequency_penalty_step"], help=params['frequency_penalty_help'], key="frequency_penaltykey") 
            presence_penalty = st.slider(label="Set presence_penalty:", min_value=params['presence_penalty_min'], max_value=params['presence_penalty_max'], value=st.session_state.presencepenalty,
                                                step=params["presence_penalty_step"], help=params['presence_penalty_help'], key="presence_penaltykey")
            # Save the chosen parameters to the system state upon submission
            st.form_submit_button("Save Parameters",on_click=helpers.save_session_state)

    st.button("Clear All Settings and Chat",on_click=lambda: st.session_state.clear())

if st.session_state['messages']:
    for message in st.session_state.messages:
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


# ###UPDATE 07/16/2023 - Add in ability to pass parameters for apim endpoint, key, and aoai_version
'''
import argparse
import os
import streamlit as st

# Define the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--apim-endpoint', type=str, required=True, help='The Azure OpenAI API Management endpoint')
parser.add_argument('--apim-key', type=str, required=True, help='The Azure OpenAI API Management key')
args = parser.parse_args()

# Set the environment variables
os.environ['APIM_ENDPOINT'] = args.apim_endpoint
os.environ['APIM_KEY'] = args.apim_key

# Define the Streamlit app
def main():
    # Your Streamlit app code here
    pass

if __name__ == '__main__':
    main()
'''