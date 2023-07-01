import openai
import streamlit as st
#do this to load the env variables
from dotenv import load_dotenv


load_dotenv()

# Set up OpenAI
openai.api_type = "azure"
openai.api_key=env['APIM_KEY']
openai.api_base=env['APIM_ENDPOINTS']
openai.api_version =['APIM_VERSION']

# The code gets the response from OpenAI, formats it, and writes it to the result box
def get_openai_response(prompt, max_tokens=max_tokens, temperature=temperature, model=model, streaming=streaming):
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

def get_openai_Chat(messages,max_tokens=max_tokens,temperature=temperature,model=model,streaming=streaming):
    try:
        # If streaming, loop through the response and append to a list
        if streaming == "Streaming":
            report = []
            # Looping over the response
            for resp in openai.ChatCompletion.create(engine=model,
                                                    messages=messages,
                                                    max_tokens=max_tokens, 
                                                    temperature = temperature,
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

# You can also use radio buttons instead
options=["Streaming", "No Streaming"]
# selected = st.radio("Choose the app", range(len(options)), format_func=lambda x: options[x])
selected = st.radio("Choose whether to stream responses or not:", options)

callEndpoints=["Completion", "Chat"]
endpointOpt = st.radio("Choose whether you wish to engage in a ChatCompletions or Completions interaction:",callEndpoints)

user_input = st.text_input("You: ", placeholder = "Ask me anything ...", value="Tell me a short joke",key="input")

if st.button("Submit", type="primary"):
    st.markdown("----")

    res_box = st.empty()
    exp = st.expander("See more info")

    messages=[]
    messages.append({"role":"user","content":user_input})

    streamIt= True if selected == "Streaming" else False
        if endpointOpt == "Completion":
            get_openai_response(user_input, max_tokens=120, temperature = 0.5,model="text-davinci-003",streaming=streamIt)
        else:
            get_openai_Chat(messages, max_tokens=120, temperature = 0.5,model="gpt-35-turbo",streaming=streamIt)

st.markdown("----")