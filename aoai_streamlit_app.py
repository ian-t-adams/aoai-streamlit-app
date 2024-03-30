import os    
import streamlit as st    
import json    
from dotenv import load_dotenv      
from openai import AzureOpenAI    
from src import aoai_helpers as helpers    
    
load_dotenv()      
    
apim_key = os.environ['APIM_KEY']      
apim_endpoint = os.environ['APIM_ENDPOINT']      
version_of_api = os.environ['AOAI_API_VERSION']    
    
client = AzureOpenAI(    
  azure_endpoint=apim_endpoint,     
  api_key=apim_key,      
  api_version=version_of_api    
)    
    
# Create containers for the header, chat window, and footer - will use sidebar for setting model parameters    
header_container = st.container()    
chat_container = st.container()    
footer_container = st.container()    
settings_container = st.sidebar.container()    
standard_system_message = "You are an AI assistant that helps people."    
    
# Top level title and description of the app    
with header_container:    
    st.title("Interact with an Azure OpenAI 🤖", anchor="top", help='''This demo showcases the Azure OpenAI Service, Azure API Management Service,    
          and Azure Web Apps with Streamlit.''')    
    
# Initialize the client in the st.session_state    
if 'client' not in st.session_state:    
    st.session_state.client = client    
    
# Initialize 'engine' in session_state if not present  
if 'engine' not in st.session_state:  
    st.session_state.engine = 'gpt-35-turbo-16k'  # Default value  
    
# Pull up the messages if they exist - needed    
if 'messages' not in st.session_state:    
    helpers.env_to_st_session_state('SYSTEM','system', standard_system_message)    
    st.session_state.messages = []    
    st.session_state.messages.append({"role":"system","content":st.session_state.system})    
    
# Load model configurations from JSON    
with open("configs/aoai_model_configs.json", "r") as f:    
    model_configs = json.load(f)    
    
with st.sidebar.title("Model Parameters", anchor="top", help='''The model parameters are used to control the behavior of the model.     
                      Each parameter has its own tooltip.'''):    
    with settings_container:    
        available_models = list(model_configs.keys())    
        available_models.remove("common_params")  # Exclude common parameters from model options    
    
        default_index = available_models.index("gpt-35-turbo-16k")    
    
        model = st.sidebar.selectbox("Choose a model:", available_models, key="modelkey", index=default_index,    
                                    help='''Choose the model with which you wish to interact. Defaults to gpt-35-turbo-16k.''')    
        st.session_state.engine = model  # Update the engine according to the chosen model  
    
        # Explicitly initialize session state for model parameters    
        st.session_state.temperature = st.session_state.get('temperature', 0.7)  
        st.session_state.max_tokens = st.session_state.get('max_tokens', 4000)  
        st.session_state.top_p = st.session_state.get('top_p', 0.9)  
        st.session_state.frequency_penalty = st.session_state.get('frequency_penalty', 0.0)  
        st.session_state.presence_penalty = st.session_state.get('presence_penalty', 0.0)  
    
        common_params = model_configs["common_params"]    
        specific_params = model_configs.get(model, {})    
        params = {**common_params, **specific_params}  # Merge dictionaries    
    
        system_message = st.sidebar.text_area("System Message",    
                                            value=st.session_state.system,    
                                            height=150,    
                                            key="txtSystem",    
                                            help='''Enter a system message here.''')    
    
        if system_message != st.session_state.system:    
            st.sidebar.warning('''WARNING: You have made changes to the system message.''')    
    
        # Read in the appropriate model specific parameters for the streamlit sliders    
        temperature = st.sidebar.slider("Set a Temperature:", min_value=params['temp_min'], max_value=params['temp_max'], value=st.session_state.temperature,    
                                        step=params['temp_step'], help=params['temp_help'], key="tempkey")    
        max_tokens = st.sidebar.slider("Set Max Tokens per Response:", min_value=params['tokens_min'], max_value=params['tokens_max'], value=st.session_state.max_tokens,    
                                       step=params['tokens_step'], help=params['tokens_help'], key="tokenskey")    
        top_p = st.sidebar.slider("Set a Top P:", min_value=params['top_p_min'], max_value=params['top_p_max'], value=st.session_state.top_p,    
                                  step=params['top_p_step'], help=params['top_p_help'], key="top_pkey")    
        frequency_penalty = st.sidebar.slider("Set a Frequency Penalty:", min_value=params['frequency_penalty_min'], max_value=params['frequency_penalty_max'], value=st.session_state.frequency_penalty,    
                                               step=params['frequency_penalty_step'], help=params['frequency_penalty_help'], key="frequency_penaltykey")    
        presence_penalty = st.sidebar.slider("Set a Presence Penalty:", min_value=params['presence_penalty_min'], max_value=params['presence_penalty_max'], value=st.session_state.presence_penalty,    
                                             step=params['presence_penalty_step'], help=params['presence_penalty_help'], key="presence_penaltykey")    
    
        if st.sidebar.button("Save Settings", key="saveButton", help='''Save the model parameter settings to the session state.''', type="primary"):        
            st.sidebar.success('Settings saved successfully!', icon="✅")    
            
        if st.sidebar.button("Clear Chat History", key="mainChatClear", help='''Clear the chat history from the session state.''', type="secondary"):    
            st.session_state.messages = []    
            st.session_state.messages.append({"role":"system","content":standard_system_message})    
            st.session_state["user_message"] = ""    
            st.session_state["assistant_message"] = ""    
            helpers.save_session_state()    
    
    token_counter_container = st.sidebar.container()    
    with token_counter_container:    
        st.empty()    
        st.caption(f":red[_____________________________________]")    
        model = helpers.translate_engine_to_model(st.session_state.engine)    
        system_tokens = helpers.num_tokens_from_messages([st.session_state.messages[0]], model)    
        user_tokens = helpers.num_tokens_from_messages([msg for msg in st.session_state.messages if msg["role"] == "user"], model)    
        assistant_tokens = helpers.num_tokens_from_messages([msg for msg in st.session_state.messages if msg["role"] == "assistant"], model)    
        total_tokens = system_tokens + user_tokens + assistant_tokens    
    
        st.write(f"System tokens: {system_tokens}")    
        st.write(f"User tokens: {user_tokens}")    
        st.write(f"Assistant tokens: {assistant_tokens}")    
        st.write(f"Total tokens: {total_tokens}")    
    
        max_tokens_progress = params['tokens_max']    
        progress = total_tokens / max_tokens_progress    
        st.progress(progress)    
    
with chat_container:    
    if st.session_state['messages']:    
        for message in st.session_state.messages:    
            if message["role"] != "system":    
                with st.chat_message(message["role"]):    
                    st.markdown(message["content"])      
    
    if prompt := st.chat_input("💬 Window - Go ahead and type!"):    
        st.session_state.messages.append({"role": "user", "content": prompt})    
        with st.chat_message("user"):    
            st.markdown(prompt)    
    
        with st.chat_message("assistant"):    
            message_placeholder = st.empty()    
            full_response = ""    
    
            for response in helpers.generate_chat_completion(client=st.session_state.client,    
                                                             engine=st.session_state.engine,    
                                                             messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],    
                                                            temperature=st.session_state.temperature,    
                                                            max_tokens=st.session_state.max_tokens,    
                                                            top_p=st.session_state.top_p,    
                                                            frequency_penalty=st.session_state.frequency_penalty,    
                                                            presence_penalty=st.session_state.presence_penalty,    
                                                            stop=None,    
                                                            stream=True):    
    
                if response.choices and len(response.choices) > 0:    
                    full_response += response.choices[0].delta.content or ""    
                message_placeholder.markdown(full_response + "▌")    
            message_placeholder.markdown(full_response)    
        st.session_state.messages.append({"role": "assistant", "content": full_response})    
    
with footer_container:    
    st.caption(f":red[______________________________________________________________________________________________]")    
    st.caption(f":red[NOTE: ALL SYSTEM MESSAGES, PROMPTS, AND COMPLETIONS ARE LOGGED FOR THIS DEMO. DO NOT ENTER ANY SENSITIVE INFORMATION.]")    
