import os, requests, html, tiktoken
import streamlit as st
from openai import AzureOpenAI

# ############################################################
# Azure OpenAI helper functions
# ############################################################
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

# Bing Search helper function
def bing_web_search(api_key, query: str, output_format: str ='html', **kwargs) -> str:
    """
    Perform a search using the Bing Web Search v7.0 API with error handling, support for various query parameters and
    advanced search keywords in the query. Outputs a string that can be displayed in either Markdown or HTML table format
    and including additional details about the search results.

    Args:
        api_key (str): The API key for accessing the Bing Web Search API.
        query (str): The user's search query term. Must not be empty.
        output_format (str): The format of the output, either 'markdown' or 'html'. Default is 'html'.
        **kwargs: Arbitrary keyword arguments representing additional query parameters supported by the API.
        advanced key words found here: https://support.microsoft.com/en-us/topic/advanced-search-keywords-ea595928-5d63-4a0b-9c6b-0b769865e78a

    Returns:
        str: A table with the search results in the specified format or an error message, including additional details.

    Example:
        >>> api_key = 'YOUR_BING_API_KEY'
        >>> query = 'How do I use tools and function calling? site:https://learn.microsoft.com/'
        >>> output = bing_web_search(api_key, query, output_format='html', count=50, mkt='en-US')
        >>> display(HTML(output))
    """  
    base_url = "https://api.bing.microsoft.com/v7.0/search"  
    headers = {"Ocp-Apim-Subscription-Key": api_key}  
    params = {"q": query}  
    params.update(kwargs)  
  
    try:  
        response = requests.get(base_url, headers=headers, params=params)  
        response.raise_for_status()  
    except requests.exceptions.HTTPError as err:  
        return f"HTTP Error: {err}"  
    except requests.exceptions.RequestException as e:  
        return f"Error: {e}"  
  
    results = response.json()  
  
    if 'webPages' not in results:  
        return "No results found or the query was invalid."  
  
    if output_format == 'markdown':  
        table = "Name (URL) | Snippet | Last Updated | Type\n"  
        table += "--- | --- | --- | ---\n"  
    elif output_format == 'html':  
        table = "<table><tr><th>Name (URL)</th><th>Snippet</th><th>Last Updated</th><th>Type</th></tr>"  
  
    for item in results.get("webPages", {}).get("value", []):  
        name = html.escape(item.get("name", "N/A"))  
        url = item.get("url", "N/A")  
        snippet = item.get("snippet", "N/A").replace("\n", " ")  
        last_updated = item.get("dateLastCrawled", "N/A")[:10]  # Extract just the date  
        result_type = "Web page"  # In this context, all results are web pages  
          
        # Handle snippet highlighting  
        if output_format == 'html':  
            snippet = html.escape(snippet, quote=False)  
        else:  # For Markdown, convert highlight tags from HTML to Markdown if present  
            snippet = snippet.replace('<strong>', '**').replace('</strong>', '**')  
          
        # Format the name and URL as a clickable link  
        if output_format == 'html':  
            link = f"<a href='{url}'>{name}</a>"  
        else:  # Markdown  
            link = f"[{name}]({url})"  
          
        # Build the table row  
        if output_format == 'markdown':  
            table += f"{link} | {snippet} | {last_updated} | {result_type}\n"  
        elif output_format == 'html':  
            table += f"<tr><td>{link}</td><td>{snippet}</td><td>{last_updated}</td><td>{result_type}</td></tr>"  
  
    table += "</table>" if output_format == 'html' else ""  
  
    return table

# ############################################################
# Tiktoken helper functions
# ############################################################
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

# ############################################################
# Streamlit session state helper functions
# ############################################################
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
    """  
    Loads settings for the sidebar options, API configurations, and model parameters.  
    Ensures that default values are used only if session state variables are not already set.  
    """  
    # Model parameters initialization  
    model_parameters = {  
        'temperature': 0.7,  
        'maxtokens': 4000,  
        'topp': 0.90,  
        'frequencypenalty': 0.0,  
        'presencepenalty': 0.0,  
        'engine': 'gpt-35-turbo-16k',  # Default model  
        'system': 'You are an AI assistant that helps people.'  
    }  
    for param, default_value in model_parameters.items():  
        if param not in st.session_state:  
            st.session_state[param] = default_value  
  
    # API settings initialization (only if reload_api_settings is True)  
    if reload_api_settings:  
        api_settings = {  
            'apiversion': '2023-12-01-preview',  
            'apikey': '',  
            'apiendpoint': ''  
        }  
        for setting, default_value in api_settings.items():  
            env_to_st_session_state(setting.upper(), setting, default_value)  

def toggle_settings():
    st.session_state['show_settings'] = not st.session_state['show_settings']

def save_session_state():  
    # Update this function to only save variables that are used and initialized within the app  
    st.session_state.client = st.session_state.client  
    st.session_state.engine = st.session_state.engine  
    st.session_state.temperature = st.session_state.temperature  
    st.session_state.max_tokens = st.session_state.max_tokens  
    st.session_state.top_p = st.session_state.top_p  
    st.session_state.frequency_penalty = st.session_state.frequency_penalty  
    st.session_state.presence_penalty = st.session_state.presence_penalty  
    st.session_state.system = st.session_state.system  
    # Update the system message in the first message if it is of type 'system'  
    if st.session_state.messages and st.session_state.messages[0]['role'] == 'system':  
        st.session_state.messages[0]['content'] = st.session_state.system  
