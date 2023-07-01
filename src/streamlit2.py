
import openai
import streamlit as st
#do this to load the env variables
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI
openai.api_type="azure"
openai.api_key=env['APIM_KEY']
openai.api_base=env['APIM_ENDPOINTS']
openai.api_version =['APIM_VERSION']

# The code gets the response from OpenAI, formats it, and writes it to the result box
def get_openai_response(prompt, max_tokens, temperature, model, streaming):
    try:
        # If streaming, loop through the response and append to a list
        if streaming == "Streaming":
            report = []
            # Looping over the response
            for resp in openai.Completion.create(engine=model,
                                                prompt=prompt,
                                                max_tokens=max_tokens, 
                                                temperature=temperature,
                                                n=1,
                                                stream=True):
                report.append(resp['choices'][0]['text'])
                result = "".join(report).strip()
                result = result.replace("\n", "")       
                res_box.markdown(f'*{result}*') 

        # If not streaming, get the response and write to the result box
        else:
            completions = openai.Completion.create(engine=model,
                                                prompt=prompt,
                                                max_tokens=max_tokens, 
                                                temperature=temperature,
                                                stream=False)
            result = completions.choices[0].text

            res_box.write(result)
    # Catch OpenAI rate limit errors
    except openai.error.RateLimitError as e:
        raise e

def get_openai_Chat(messages, max_tokens, temperature, model, streaming):
    try:
        # If streaming, loop through the response and append to a list
        if streaming == "Streaming":
            report = []
            # Looping over the response
            for resp in openai.ChatCompletion.create(engine=model,
                                                    messages=messages,
                                                    max_tokens=max_tokens, 
                                                    temperature=temperature,
                                                    stream=True):
                if 'content' in resp['choices'][0]['delta']:
                    report.append(resp['choices'][0]['delta']['content'])
                    result = "".join(report).strip()
                    result = result.replace("\n", "")       
                    res_box.markdown(f'*{result}*') 

        # If not streaming, get the response and write to the result box
        else:
            completions = openai.ChatCompletion.create(engine=model,
                                                        messages=messages,
                                                        max_tokens=max_tokens, 
                                                        temperature=temperature,
                                                        stream=False)
            result = completions.choices[0].message.content

            res_box.write(result)
    except openai.error.RateLimitError as e:
        raise e       

st.subheader("Chat, Stream, Retry")  
  
options=["Streaming", "No Streaming"]  
selected = st.radio("Choose whether to stream responses or not:", options)  
  
callEndpoints=["Chat", "Completion", "Embedding"]  
endpointOpt = st.radio("Choose whether you wish to engage in a Chat (ChatCompletions) or Completions interaction for text or Embeddings for a demonstration of embeddings outputs:",callEndpoints)  
  
if endpointOpt == "Chat":  
    model_options = ["gpt-35-turbo", "gpt-4", "gpt-4-32k"]  
elif endpointOpt == "Completion":  
    model_options = ["text-davinci-003"]  
else:  
    model_options = ["text-embedding-ada-002"]  
model = st.selectbox("Choose a model:", model_options)  
  
# Max tokens selection with Streamlit slider  
if model == "gpt-35-turbo":  
    max_tokens = st.slider("Choose max tokens:", min_value=10, max_value=4000, step=10)
    temp_options = st.slider("Choose a temperature:", min_value=0, max_value=2, step=0.01)
    top_p_options = st.slider("Choose a top p:", min_value=0, max_value=1, step=0.01)
elif model == "gpt-4":
    max_tokens = st.slider("Choose max tokens:", min_value=10, max_value=8190, step=10)
    temp_options = st.slider("Choose a temperature:", min_value=0, max_value=2, step=0.01)
elif model == "gpt-4-32k":
    max_tokens = st.slider("Choose max tokens:", min_value=10, max_value=32760, step=10)
    temp_options = st.slider("Choose a temperature:", min_value=0, max_value=2, step=0.01)
elif model == "text-davinci-003":
    max_tokens = st.slider("Choose max tokens:", min_value=10, max_value=4000, step=10)
    temp_options = st.slider("Choose a temperature:", min_value=0, max_value=1, step=0.01)
else:
    max_tokens = st.slider("Choose max tokens:", min_value=10, max_value=4000, step=10)
    temp_options = st.slider("Choose a temperature:", min_value=0, max_value=0, step=0)  
  
user_input = st.text_input("You: ", placeholder = "Ask me anything ...", value="Tell me a short joke",key="input")  
  
if st.button("Submit", type="primary"):  
    st.markdown("----")

    res_box = st.empty()
    exp = st.expander("See more info")

    messages=[]
    messages.append({"role":"user","content":user_input})

    streaming=True if selected == "Streaming" else False
    if endpointOpt == "Completion":
        get_openai_response(user_input, max_tokens, temp_options, model, streaming)
    else:
        get_openai_Chat(messages, max_tokens, temp_options, model, streaming)

st.markdown("----")
