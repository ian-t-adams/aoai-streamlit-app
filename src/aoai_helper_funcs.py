import openai
import tiktoken
import streamlit as st

def generate_chat_completion(engine, messages, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop, stream):
    '''
    Generates a chat completion based on the provided messages.
    '''
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            stream=stream
        )
        return response
    except openai.error.RateLimitError as e:
        raise e
    
def generate_completion(engine, prompt, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop, stream):
    '''
    Generates a completion based on the provided prompt.
    '''
    try:
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            stream=stream
        )
        return response
    except openai.error.RateLimitError as e:
        raise e

def translate_engine_to_model(engine):
    '''
    Translates the engine name to the model name for use with 
    tiktoken.encoding_for_model for token tracking.
    '''
    try:
        engine_model_dict = {"gpt-35-turbo": "gpt-3.5-turbo",
                             "gpt-35-turbo-16k": "gpt-3.5-turbo-16k-0613",
                             "gpt-4": "gpt-4-0613",
                             "gpt-4-32k": "gpt-4-32k-0613"}
        model = engine_model_dict[engine]
        return model
    except KeyError:
        raise KeyError(f"Engine {engine} not found. Please use one of the following: {engine_model_dict.keys()}")

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

def available_models():
    '''
    Returns a list of available models.
    '''
    # Create a dictionary containing the available models for each completion type  
    available_models = {  
        "Chat": ["gpt-4", "gpt-4-32k", "gpt-35-turbo", "gpt-35-turbo-16k"],  
        "Completion": ["text-davinci-003"],  
        #"Embedding": ["text-embedding-ada-002"]  
    }
    return ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"]

def streamlit_sidebar_options(engine)
    