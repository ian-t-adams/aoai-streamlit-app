# aoai-streamlit-app

Azure hosted Streamlit App centered around Azure OpenAI Service LLM's

>Note: Borrowed heavily from my colleague [Kirk's repo](https://github.com/kirkhofer/data-ai/blob/main/aoai/chat.py) As well as from the [Microsoft OpenAI Workshop content](https://github.com/microsoft/OpenAIWorkshop)

## To run quickly

1. Clone this repo

2. Create a .env in the main folder file and add in the following parameters:

        APIM_ENDPOINT={whatever your openai endpoint is}

        APIM_KEY={your Azure OpenAI Key}

        AOAI_API_VERSION=2023-05-15

3. Install the necessary Python dependencies

4. Run:

    > streamlit run C:\{path\to\aoai-streamlit-app\repo}\aoai_streamlit_app.py

5. Enjoy

## Things to add or do

1. Persistent stateliness - Cosmos?
2. Prompt Flow tracking? Prompt versioning - Delta lake?
3. Rate responses / Human-in-the-loop / feedback loop
4. ???
