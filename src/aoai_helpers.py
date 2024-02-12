import os
import time
import tiktoken
import requests
import streamlit as st
from datetime import datetime
from IPython.display import HTML
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
def get_web_search_results(query: str, bing_subscription_key: str, bing_search_url: str, answer_count: int = None, country_code: str = None, result_count: int = 50, result_freshness: str = None, market: str = "en-US", page_offset: int = None, promote_result_type: list[str] = None, response_filter: list[str] = None, safe_search: str = "Off", set_language: str = None, text_decorations: bool = True, text_format: str = "HTML"):
    """
    Executes a web search using the Bing Web Search API v7 and returns the results in an HTML table format.

    This function sends a request to the Bing Web Search API with the provided query and other optional search parameters.
    It then processes the API response and formats the search results as an HTML table with headers for URL, Snippet, 
    Date Published, and Result Freshness. If no results are found or an error occurs, an appropriate message is returned.

    Args:
        query (str): The user's search query string.
        bing_subscription_key (str): The subscription key for accessing the Bing Web Search API.
        bing_search_url (str): The URL endpoint for the Bing Web Search API.
        answer_count (int, optional): The number of answers that you want the search API to return.
        country_code (str, optional): A 2-character country code of the country where the results come from.
        result_count (int, optional): The number of search results to return in the response.
        result_freshness (str, optional): Filter search results based on age. Possible values are "Day", "Week", "Month".
        market (str, optional): The market where the results come from. Typically, mkt is the country where the user is making the request from.
        page_offset (int, optional): The number of search results to skip before returning results.
        promote_result_type (list[str], optional): A list of answer types to promote at the top of the search results.
        response_filter (list[str], optional): A comma-delimited list of answer types to return in the search results.
        safe_search (str, optional): A filter used to filter webpages for adult content. Possible values are "Off", "Moderate", "Strict".
        set_language (str, optional): The language to use for user interface strings.
        text_decorations (bool, optional): A Boolean value that determines whether display strings contain decoration markers such as hit highlighting characters.
        text_format (str, optional): The format of the response. Possible values are "Raw", "HTML".

    Returns:
        IPython.core.display.HTML: An HTML object that contains a table of the search results. Each row of the table represents a single search result, including the URL, a snippet, the date published, and the result freshness.

    Raises:
        Exception: If there is an issue with the API request or processing the response, an exception is printed and returned.

    Example:
        >>> html_results = get_web_search_results(
                query="Python programming",
                bing_subscription_key="YOUR_SUBSCRIPTION_KEY",
                bing_search_url="https://api.cognitive.microsoft.com/bing/v7.0/search",
                result_count=10,
                market="en-US",
                safe_search="Strict"
            )
        >>> display(html_results)

    Note:
        To use this function, you must have a valid Bing Web Search API subscription key.
        Ensure that you are complying with the Bing Web Search API terms of use.
    """
    try:
        # Create the header object with the subscription key
        headers = {"Ocp-Apim-Subscription-Key": bing_subscription_key}
        # Create a dictionary of the required and optional parameters for the API request
        # Start with the required query parameter
        params = {"q": query}  # Start with the required query parameter

        # Add optional parameters to the params dictionary if they are not None
        if answer_count is not None:
            params["answerCount"] = answer_count
        if country_code is not None:
            params["cc"] = country_code
        if result_count is not None:
            params["count"] = result_count
        if result_freshness is not None:
            params["freshness"] = result_freshness
        if market is not None:
            params["mkt"] = market
        if page_offset is not None:
            params["offset"] = page_offset
        if promote_result_type is not None:
            params["promote"] = promote_result_type
        if response_filter is not None:
            params["responseFilter"] = response_filter
        if safe_search is not None:
            params["safeSearch"] = safe_search
        if set_language is not None:
            params["setLang"] = set_language
        if text_decorations is not None:
            params["textDecorations"] = text_decorations
        if text_format is not None:
            params["textFormat"] = text_format

        # Send the request to the Bing Web Search API
        response = requests.get(bing_search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()

        # Format the search results as an HTML table
        header = "<tr><th>URL</th><th>Snippet</th><th>Date Published</th><th>Result Freshness</th></tr>"
        # Extract the search results and format them as rows of an HTML table
        if 'webPages' in search_results and 'value' in search_results['webPages']:
            rows = "\n".join([f"""<tr>
                                  <td><a href=\"{v.get("url", "URL not available")}\">{v.get("name", "Name not available")}</a></td>
                                  <td>{v.get("snippet", "Snippet not available")}</td>
                                  <td>{datetime.strptime(v.get("datePublished", "0001-01-01T00:00:00Z")[:-1], '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d') if v.get("datePublished") else "Date not available"}</td>
                                  <td>{v.get("datePublishedFreshnessText", "Not available")}</td>
                              </tr>"""
                        for v in search_results["webPages"]["value"]])
        else:
            rows = "No results found."
        
        # Prepend the header to the rows
        rows = header + rows

        # Retun the table with HTML mark-up
        html_table = HTML("<table>{0}</table>".format(rows))
        return html_table

    except Exception as e:
        print("An error occurred during the web search.")
        return e

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
