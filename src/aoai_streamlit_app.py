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
        "Embedding": ["text-embedding-ada-002"]  
    }

    callEndpoints = ["Chat", "Completion", "Embedding"]  
    completion_type = st.sidebar.radio(  
        "Choose whether you wish to engage in a Chat (ChatCompletions) or Completions interaction for text or Embeddings for a demonstration of embeddings outputs:",  
        callEndpoints)

    # Update the model_options depending on the selected completion type  
    model_options = available_models[completion_type]    
  
    models_explanation = st.sidebar.expander("Models Explanation")  
    models_explanation.write("Different AI models have different capabilities and limitations. Some models may be better suited for specific tasks, while others may offer faster response times or more creative responses. Choose a model that best fits your needs.")  
      
    model = st.sidebar.selectbox("Choose a model:", model_options)  
  
    max_tokens_explanation = st.sidebar.expander("Max Tokens Explanation")  
    max_tokens_explanation.write("Max tokens determine the maximum length of the AI response. A larger value allows for longer, more detailed responses, while a smaller value will limit the response to a shorter length.")  
  
    max_tokens = st.sidebar.slider("Choose max tokens:", min_value=10, max_value=4000, step=10)  
  
    temperature_explanation = st.sidebar.expander("Temperature Explanation")  
    temperature_explanation.write("Temperature affects the randomness of the AI response. A higher temperature will result in more random and creative responses, while a lower temperature will produce more focused and deterministic responses.")  
  
    temp_options = st.sidebar.slider("Choose a temperature:", min_value=0.00, max_value=2.00, step=0.01)  
  
    options = ["Streaming", "No Streaming"]  
    selected = st.sidebar.radio("Choose whether to stream responses or not:", options)  
  
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
