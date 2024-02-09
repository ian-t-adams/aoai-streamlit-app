import os
import time
import tiktoken
import streamlit as st
from openai import AzureOpenAI

def generate_chat_completion(client, engine, messages, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop, stream):
    '''
    Generates a chat completion based on the provided messages.
    '''
    try:
        response = client.chat.completions.create(
            model=engine,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            stream=stream
        )
        return response
    except AzureOpenAI.error.RateLimitError as e:
        raise e

def translate_engine_to_model(engine):
    '''
    Translates the engine name to the model name for use with 
    tiktoken.encoding_for_model for token tracking.
    '''
    try:
        engine_model_dict = {"gpt-35-turbo-0301" : "gpt-3.5-turbo",
							 "gpt-35-turbo-0613" : "gpt-3.5-turbo",
							 "gpt-35-turbo-1106" : "gpt-3.5-turbo",
							 "gpt-35-turbo-16k" : "gpt-3.5-turbo-16k-0613",
							 "gpt-4" : "gpt-4-0613",
							 "gpt-4-32k" : "gpt-4-32k-0613",
							 "gpt-4-turbo" : "gpt-4-32k-0613"}
        model = engine_model_dict.get(engine)
        if model is None:
            raise KeyError(f"Engine {engine} not found. Please use one of the following: {list(engine_model_dict.keys())}")
        return model
    except KeyError:
        engine_model_dict = {"gpt-35-turbo-0301" : "gpt-3.5-turbo",
							 "gpt-35-turbo-0613" : "gpt-3.5-turbo",
							 "gpt-35-turbo-1106" : "gpt-3.5-turbo",
							 "gpt-35-turbo-16k" : "gpt-3.5-turbo-16k-0613",
							 "gpt-4" : "gpt-4-0613",
							 "gpt-4-32k" : "gpt-4-32k-0613",
							 "gpt-4-turbo" : "gpt-4-32k-0613"}
        raise KeyError(f"Engine {engine} not found. Please use one of the following: {list(engine_model_dict.keys())}")

def num_tokens_from_messages(messages, model):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def env_to_st_session_state(setting_name, session_name, default_value):  
    """  
    Function to generate st.session_state variables from environment variables.  
    """  
    if session_name not in st.session_state:  
        if os.environ.get(setting_name) is not None:
            st.session_state[session_name] = os.environ.get(setting_name)
        else:
            st.session_state[session_name] = default_value

def load_settings(reload_api_settings=True):
    # These set the default values for the sidebar optoins and are used in aoai_streamlit_app.py
    # This is what values return to when reset is clicked
    env_to_st_session_state('ST_ENGINE', 'engine', 'gpt-35-turbo-16k')
    env_to_st_session_state('ST_TEMPERATURE', 'temperature', 0.5)
    env_to_st_session_state('ST_MAX_TOKENS', 'maxtokens', 4000)
    env_to_st_session_state('ST_TOP_P', 'topp', 0.90)
    env_to_st_session_state('ST_FREQUENCY_PENALTY', 'frequencypenalty', 0.0)
    env_to_st_session_state('ST_PRESENCE_PENALTY', 'presencepenalty', 0.0)

    # These are the default values for the API settings
    # only loaded if reload_api_settings = True
    if reload_api_settings:
        # Load in the API settings if requested
        env_to_st_session_state('AOAI_API_VERSION', 'apiversion', '2023-12-01-preview')
        env_to_st_session_state('APIM_KEY', 'apikey', '')
        env_to_st_session_state('APIM_ENDPOINT', 'apiendpoint', '')

def toggle_settings():
    st.session_state['show_settings'] = not st.session_state['show_settings']

def save_session_state():
    st.session_state.apiversion = st.session_state.apiversion 
    st.session_state.apikey = st.session_state.apikey 
    st.session_state.apiendpoint = st.session_state.apiendpoint
    st.session_state.client = st.session_state.client
    st.session_state.engine = st.session_state.modelkey
    st.session_state.temperature = st.session_state.tempkey 
    st.session_state.maxtokens = st.session_state.tokenskey 
    st.session_state.topp = st.session_state.top_pkey 
    st.session_state.frequencypenalty = st.session_state.frequency_penaltykey
    st.session_state.presencepenalty = st.session_state.presence_penaltykey
    st.session_state.system = st.session_state.txtSystem 
    st.session_state.messages[0]['content'] = st.session_state.system
