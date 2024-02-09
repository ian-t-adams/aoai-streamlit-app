# Define a dictionary for  use with st.sidebar when loaded into aoai_streamlit_app.py
model_params = {  
    "gpt-35-turbo-0301": {
        "tokens_min": 10,
        "tokens_max": 4000,
        "tokens_step": 10,
        "tokens_help": '''Set a limit on the number of tokens per model response. 
        The API supports a maximum of 4000 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. 
        One token is roughly 4 characters for typical English text.''',
        "temp_min": 0.00,
        "temp_max": 2.00,
        "temp_step": 0.01,
        "temp_help": '''Controls randomness. Lowering the temperature means that the model will produce more repetitive and deterministic responses.
         Increasing the temperature will result in more unexpected or creative responses. Try adjusting temperature or Top P but not both.''',
        "top_p_min": 0.00,
        "top_p_max": 1.00,
        "top_p_step": 0.01,
        "top_p_help": '''Similar to temperature, this controls randomness but uses a different method, called nucleus sampling where
        the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 
        10% probability mass are considered. Lowering Top P will narrow the model’s token selection to likelier tokens. 
        Increasing Top P will let the model choose from tokens with both high and low likelihood. 
        Try adjusting temperature or Top P but not both.''',
        "frequency_penalty_min": -2.00,
        "frequency_penalty_max": 2.00,
        "frequency_penalty_step": 0.01,
        "frequency_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating a token proportionally based on how often it has appeared in the text so far. 
        This decreases the likelihood of repeating the exact same text in a response..''',
        "presence_penalty_min": -2.00,
        "presence_penalty_max": 2.00,
        "presence_penalty_step": 0.01,
        "presence_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating any token that has appeared in the text at all so far. 
        This increases the likelihood of introducing new topics in a response.''',
        },
    "gpt-35-turbo-0613": {
        "tokens_min": 10,
        "tokens_max": 4000,
        "tokens_step": 10,
        "tokens_help": '''Set a limit on the number of tokens per model response. 
        The API supports a maximum of 4000 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. 
        One token is roughly 4 characters for typical English text.''',
        "temp_min": 0.00,
        "temp_max": 2.00,
        "temp_step": 0.01,
        "temp_help": '''Controls randomness. Lowering the temperature means that the model will produce more repetitive and deterministic responses.
         Increasing the temperature will result in more unexpected or creative responses. Try adjusting temperature or Top P but not both.''',
        "top_p_min": 0.00,
        "top_p_max": 1.00,
        "top_p_step": 0.01,
        "top_p_help": '''Similar to temperature, this controls randomness but uses a different method, called nucleus sampling where
        the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 
        10% probability mass are considered. Lowering Top P will narrow the model’s token selection to likelier tokens. 
        Increasing Top P will let the model choose from tokens with both high and low likelihood. 
        Try adjusting temperature or Top P but not both.''',
        "frequency_penalty_min": -2.00,
        "frequency_penalty_max": 2.00,
        "frequency_penalty_step": 0.01,
        "frequency_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating a token proportionally based on how often it has appeared in the text so far. 
        This decreases the likelihood of repeating the exact same text in a response..''',
        "presence_penalty_min": -2.00,
        "presence_penalty_max": 2.00,
        "presence_penalty_step": 0.01,
        "presence_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating any token that has appeared in the text at all so far. 
        This increases the likelihood of introducing new topics in a response.''',
        },
    "gpt-35-turbo-1106": {
        "tokens_min": 10,
        "tokens_max": 16000,
        "tokens_step": 10,
        "tokens_help": '''Set a limit on the number of tokens per model response. 
        The API supports a maximum of 4000 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. 
        One token is roughly 4 characters for typical English text.''',
        "temp_min": 0.00,
        "temp_max": 2.00,
        "temp_step": 0.01,
        "temp_help": '''Controls randomness. Lowering the temperature means that the model will produce more repetitive and deterministic responses.
         Increasing the temperature will result in more unexpected or creative responses. Try adjusting temperature or Top P but not both.''',
        "top_p_min": 0.00,
        "top_p_max": 1.00,
        "top_p_step": 0.01,
        "top_p_help": '''Similar to temperature, this controls randomness but uses a different method, called nucleus sampling where
        the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 
        10% probability mass are considered. Lowering Top P will narrow the model’s token selection to likelier tokens. 
        Increasing Top P will let the model choose from tokens with both high and low likelihood. 
        Try adjusting temperature or Top P but not both.''',
        "frequency_penalty_min": -2.00,
        "frequency_penalty_max": 2.00,
        "frequency_penalty_step": 0.01,
        "frequency_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating a token proportionally based on how often it has appeared in the text so far. 
        This decreases the likelihood of repeating the exact same text in a response..''',
        "presence_penalty_min": -2.00,
        "presence_penalty_max": 2.00,
        "presence_penalty_step": 0.01,
        "presence_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating any token that has appeared in the text at all so far. 
        This increases the likelihood of introducing new topics in a response.''',
        },
    "gpt-35-turbo-16k": {
        "tokens_min": 10,
        "tokens_max": 16000,
        "tokens_step": 10,
        "tokens_help": '''Set a limit on the number of tokens per model response. 
        The API supports a maximum of 16,000 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. 
        One token is roughly 4 characters for typical English text.''',
        "temp_min": 0.00,
        "temp_max": 2.00,
        "temp_step": 0.01,
        "temp_help": '''Controls randomness. Lowering the temperature means that the model will produce more repetitive and deterministic responses.
         Increasing the temperature will result in more unexpected or creative responses. Try adjusting temperature or Top P but not both.''',
        "top_p_min": 0.00,
        "top_p_max": 1.00,
        "top_p_step": 0.01,
        "top_p_help": '''Similar to temperature, this controls randomness but uses a different method, called nucleus sampling where
        the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 
        10% probability mass are considered. Lowering Top P will narrow the model’s token selection to likelier tokens. 
        Increasing Top P will let the model choose from tokens with both high and low likelihood. 
        Try adjusting temperature or Top P but not both.''',
        "frequency_penalty_min": -2.00,
        "frequency_penalty_max": 2.00,
        "frequency_penalty_step": 0.01,
        "frequency_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating a token proportionally based on how often it has appeared in the text so far. 
        This decreases the likelihood of repeating the exact same text in a response..''',
        "presence_penalty_min": -2.00,
        "presence_penalty_max": 2.00,
        "presence_penalty_step": 0.01,
        "presence_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating any token that has appeared in the text at all so far. 
        This increases the likelihood of introducing new topics in a response.''',
        },
    "gpt-4": {
        "tokens_min": 10,
        "tokens_max": 8192,
        "tokens_step": 10,
        "tokens_help": '''Set a limit on the number of tokens per model response. 
        The API supports a maximum of 8,192 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. 
        One token is roughly 4 characters for typical English text.''',
        "temp_min": 0.00,
        "temp_max": 2.00,
        "temp_step": 0.01,
        "temp_help": '''Controls randomness. Lowering the temperature means that the model will produce more repetitive and deterministic responses.
         Increasing the temperature will result in more unexpected or creative responses. Try adjusting temperature or Top P but not both.''',
        "top_p_min": 0.00,
        "top_p_max": 1.00,
        "top_p_step": 0.01,
        "top_p_help": '''Similar to temperature, this controls randomness but uses a different method, called nucleus sampling where
        the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 
        10% probability mass are considered. Lowering Top P will narrow the model’s token selection to likelier tokens. 
        Increasing Top P will let the model choose from tokens with both high and low likelihood. 
        Try adjusting temperature or Top P but not both.''',
        "frequency_penalty_min": -2.00,
        "frequency_penalty_max": 2.00,
        "frequency_penalty_step": 0.01,
        "frequency_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating a token proportionally based on how often it has appeared in the text so far. 
        This decreases the likelihood of repeating the exact same text in a response..''',
        "presence_penalty_min": -2.00,
        "presence_penalty_max": 2.00,
        "presence_penalty_step": 0.01,
        "presence_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating any token that has appeared in the text at all so far. 
        This increases the likelihood of introducing new topics in a response.''',
        },
    "gpt-4-32k": {
        "tokens_min": 10,
        "tokens_max": 32768,
        "tokens_step": 10,
        "tokens_help": '''Set a limit on the number of tokens per model response. 
        The API supports a maximum of 32,768 tokens shared between the prompt (including system message, examples, message history, and user query) and the model's response. 
        One token is roughly 4 characters for typical English text.''',
        "temp_min": 0.00,
        "temp_max": 2.00,
        "temp_step": 0.01,
        "temp_help": '''Controls randomness. Lowering the temperature means that the model will produce more repetitive and deterministic responses.
         Increasing the temperature will result in more unexpected or creative responses. Try adjusting temperature or Top P but not both.''',
        "top_p_min": 0.00,
        "top_p_max": 1.00,
        "top_p_step": 0.01,
        "top_p_help": '''Similar to temperature, this controls randomness but uses a different method, called nucleus sampling where
        the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 
        10% probability mass are considered. Lowering Top P will narrow the model’s token selection to likelier tokens. 
        Increasing Top P will let the model choose from tokens with both high and low likelihood. 
        Try adjusting temperature or Top P but not both.''',
        "frequency_penalty_min": -2.00,
        "frequency_penalty_max": 2.00,
        "frequency_penalty_step": 0.01,
        "frequency_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating a token proportionally based on how often it has appeared in the text so far. 
        This decreases the likelihood of repeating the exact same text in a response..''',
        "presence_penalty_min": -2.00,
        "presence_penalty_max": 2.00,
        "presence_penalty_step": 0.01,
        "presence_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating any token that has appeared in the text at all so far. 
        This increases the likelihood of introducing new topics in a response.''',
        },
    "gpt-4-turbo": {
        "tokens_min": 10,
        "tokens_max": 4096,
        "tokens_step": 10,
        "tokens_help": '''Set a limit on the number of tokens per model response. 
        The API supports a maximum of 4,096 tokens for it's output. HOWEVER, it has a 128,000 token context window, so large amounts of text may be submitted but it will
        still be limited to the 4,096 max token output in a single response. You can ask it to continue to keep providing output if it cuts off mid-sentence.''',
        "temp_min": 0.00,
        "temp_max": 2.00,
        "temp_step": 0.01,
        "temp_help": '''Controls randomness. Lowering the temperature means that the model will produce more repetitive and deterministic responses.
         Increasing the temperature will result in more unexpected or creative responses. Try adjusting temperature or Top P but not both.''',
        "top_p_min": 0.00,
        "top_p_max": 1.00,
        "top_p_step": 0.01,
        "top_p_help": '''Similar to temperature, this controls randomness but uses a different method, called nucleus sampling where
        the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 
        10% probability mass are considered. Lowering Top P will narrow the model’s token selection to likelier tokens. 
        Increasing Top P will let the model choose from tokens with both high and low likelihood. 
        Try adjusting temperature or Top P but not both.''',
        "frequency_penalty_min": -2.00,
        "frequency_penalty_max": 2.00,
        "frequency_penalty_step": 0.01,
        "frequency_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating a token proportionally based on how often it has appeared in the text so far. 
        This decreases the likelihood of repeating the exact same text in a response..''',
        "presence_penalty_min": -2.00,
        "presence_penalty_max": 2.00,
        "presence_penalty_step": 0.01,
        "presence_penalty_help": '''Number between -2.0 and 2.0. Reduce the chance of repeating any token that has appeared in the text at all so far. 
        This increases the likelihood of introducing new topics in a response.''',
        },  
    # Add more models here...  
    }
