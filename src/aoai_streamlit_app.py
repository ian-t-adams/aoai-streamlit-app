import os  
import openai  
import streamlit as st  
from dotenv import load_dotenv  
  
load_dotenv()  
  
if __name__ == "__main__":  
    openai.api_type = "azure"  
    openai.api_key = os.environ['APIM_KEY']  
    openai.api_base = os.environ['APIM_ENDPOINT']  
    openai.api_version = os.environ['AOAI_API_VERSION']  
  
    def get_openai_response(prompt, max_tokens, temperature, model, streaming):  
        try:  
            if streaming == "Streaming":  
                report = []  
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
  
            else:  
                completions = openai.Completion.create(engine=model,  
                                                       prompt=prompt,  
                                                       max_tokens=max_tokens,  
                                                       temperature=temperature,  
                                                       stream=False)  
                result = completions.choices[0].text  
  
                res_box.write(result)  
        except openai.error.RateLimitError as e:  
            raise e  
  
    def get_openai_Chat(messages, max_tokens, temperature, model, streaming):  
        try:  
            if streaming == "Streaming":  
                report = []  
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

    st.sidebar.title("Configuration")  

    # Create a dictionary containing the available models for each completion type  
    available_models = {  
        "Chat": ["gpt-4", "gpt-4-32k", "gpt-35-turbo", "gpt-35-turbo-16k"],  
        "Completion": ["text-davinci-003"],  
        #"Embedding": ["text-embedding-ada-002"]  
    }

    callEndpoints = ["Chat", "Completion"]#, "Embedding"]  
    completion_type = st.sidebar.radio(  
        "Choose whether you wish to engage in a Chat (ChatCompletions) or Completions interaction:",# for text or Embeddings for a demonstration of embeddings outputs:",  
        callEndpoints, key="uniquekey1", help="No Streaming means results display when the API call is complete. Streaming means results display as they are generated by the API. Streaming is only available for ChatCompletions and Completions.")
  
    # Update the model_options depending on the selected completion type  
    model_options = available_models[completion_type]  
    
    model = st.sidebar.selectbox("Choose a model:", model_options)  
    
    # Max tokens, temperature, and top_p selections with Streamlit sliders  
    if model == "gpt-35-turbo":  
        max_tokens = st.sidebar.slider("Choose max tokens:", min_value=10, max_value=4000, step=10, help="Set a limit on the number of tokens per model response. The API supports a maximum of 4000 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. One token is roughly 4 characters for typical English text.")
        temp_options = st.sidebar.slider("Choose a temperature:", min_value=0.00, max_value=2.00, step=0.01, help="Controls randomness. Lowering the temperature means that the model will produce more repetitive and deterministic responses. Increasing the temperature will result in more unexpected or creative responses. Try adjusting temperature or Top P but not both.")  
        top_p_options = st.sidebar.slider("Choose a top_p:", min_value=0.00, max_value=1.00, step=0.01, help="Similar to temperature, this controls randomness but uses a different method. Lowering Top P will narrow the model’s token selection to likelier tokens. Increasing Top P will let the model choose from tokens with both high and low likelihood. Try adjusting temperature or Top P but not both.")
    elif model == "gpt-35-turbo-16k":  
        max_tokens = st.sidebar.slider("Choose max tokens:", min_value=10, max_value=16000, step=10, help="Set a limit on the number of tokens per model response. The API supports a maximum of 16000 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. One token is roughly 4 characters for typical English text.")  
        temp_options = st.sidebar.slider("Choose a temperature:", min_value=0.00, max_value=2.00, step=0.01, help="Controls randomness. Lowering the temperature means that the model will produce more repetitive and deterministic responses. Increasing the temperature will result in more unexpected or creative responses. Try adjusting temperature or Top P but not both.")  
        top_p_options = st.sidebar.slider("Choose a top_p:", min_value=0.00, max_value=1.00, step=0.01, help="Similar to temperature, this controls randomness but uses a different method. Lowering Top P will narrow the model’s token selection to likelier tokens. Increasing Top P will let the model choose from tokens with both high and low likelihood. Try adjusting temperature or Top P but not both.")   
    elif model == "gpt-4":  
        max_tokens = st.sidebar.slider("Choose max tokens:", min_value=10, max_value=8190, step=10, help="Set a limit on the number of tokens per model response. The API supports a maximum of 8192 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. One token is roughly 4 characters for typical English text.")  
        temp_options = st.sidebar.slider("Choose a temperature:", min_value=0.00, max_value=2.00, step=0.01, help="Controls randomness. Lowering the temperature means that the model will produce more repetitive and deterministic responses. Increasing the temperature will result in more unexpected or creative responses. Try adjusting temperature or Top P but not both.")
        top_p_options = st.sidebar.slider("Choose a top_p:", min_value=0.00, max_value=1.00, step=0.01, help="Similar to temperature, this controls randomness but uses a different method. Lowering Top P will narrow the model’s token selection to likelier tokens. Increasing Top P will let the model choose from tokens with both high and low likelihood. Try adjusting temperature or Top P but not both.")
    elif model == "gpt-4-32k":  
        max_tokens = st.sidebar.slider("Choose max tokens:", min_value=10, max_value=32768, step=10, help="Set a limit on the number of tokens per model response. The API supports a maximum of 32768 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. One token is roughly 4 characters for typical English text.")
        temp_options = st.sidebar.slider("Choose a temperature:", min_value=0.00, max_value=2.00, step=0.01, help="Similar to temperature, this controls randomness but uses a different method. Lowering Top P will narrow the model’s token selection to likelier tokens. Increasing Top P will let the model choose from tokens with both high and low likelihood. Try adjusting temperature or Top P but not both.")
        top_p_options = st.sidebar.slider("Choose a top_p:", min_value=0.00, max_value=1.00, step=0.01, help="Similar to temperature, this controls randomness but uses a different method. Lowering Top P will narrow the model’s token selection to likelier tokens. Increasing Top P will let the model choose from tokens with both high and low likelihood. Try adjusting temperature or Top P but not both.")  
    elif model == "text-davinci-003":  
        max_tokens = st.sidebar.slider("Choose max tokens:", min_value=10, max_value=4000, step=10, help="Set a limit on the number of tokens per model response. The API supports a maximum of 4000 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. One token is roughly 4 characters for typical English text.")  
        temp_options = st.sidebar.slider("Choose a temperature:", min_value=0.00, max_value=1.00, step=0.01, help="Controls randomness. Lowering the temperature means that the model will produce more repetitive and deterministic responses. Increasing the temperature will result in more unexpected or creative responses. Try adjusting temperature or Top P but not both.")
    #elif model == "text-embedding-ada-002":
    else:  
        max_tokens = st.sidebar.slider("Choose max tokens:", min_value=10, max_value=4000, step=10)  
        temp_options = st.sidebar.slider("Choose a temperature:", min_value=0, max_value=0, step=0.01)  
  
    options = ["Streaming", "No Streaming"]  
    selected = st.sidebar.radio("Choose whether to stream responses or not:", options, key="uniquekey2")  
  
    st.subheader("Chat with AOAI!")  
    user_input = st.text_input("You: ", placeholder="Ask me anything ...", value="Tell me a short joke", key="input")  
  
    if st.button("Submit", type="primary"):  
        st.markdown("----")  
  
        res_box = st.empty()  
        exp = st.expander("See more info")  
  
        messages = []  
        messages.append({"role": "user", "content": user_input})  
  
        streaming = True if selected == "Streaming" else False  
        if completion_type == "Completion":  
            get_openai_response(user_input, max_tokens, temp_options, model, streaming)  
        else:  
            get_openai_Chat(messages, max_tokens, temp_options, model, streaming)  
  
    st.markdown("----")  
