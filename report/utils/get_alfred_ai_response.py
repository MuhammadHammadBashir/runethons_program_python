import os
import openai
import anthropic
import google.generativeai as genai

# Initialize API clients
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

def get_alfred_ai_response(prompt, model="claude", continue_response=False, previous_messages="", temperature=0):
    """
    Function to get AI-generated responses from Claude, GPT-4, or Gemini.

    :param prompt: The input prompt for the AI model.
    :param model: AI model to use ("claude", "gpt", or "gemini").
    :param continue_response: Boolean flag for continuing conversation (Claude only).
    :param previous_messages: Previous messages to continue response (Claude only).
    :param temperature: Sampling temperature for response generation.
    :return: AI-generated response as a string.
    """
    response = ""

    if model == "claude":
        response = get_claude_response(prompt, continue_response, previous_messages, temperature)
    elif model == "gpt":
        response = get_chat_gpt_response(prompt)
    elif model == "gemini":
        response = get_gemini_response(prompt)
    
    return response


def get_chat_gpt_response(prompt):
    """
    Fetch response from OpenAI's GPT-4 model.
    """
    client = openai.OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Esegui il prompt"}
        ],
        temperature=0,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content


def get_gemini_response(prompt):
    """
    Fetch response from Google's Gemini model.
    """
    genai.configure(api_key=gemini_api_key)

    # Define model parameters
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }

    # Select the model
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-002", generation_config=generation_config)



    # Generate a response
    response = model.generate_content(prompt)

    # Print the response
   
    return response.text


def get_claude_response(prompt, continue_response=False, previous_messages="", temperature=0):
    """
    Fetch response from Anthropic's Claude model.
    """
    client = anthropic.Anthropic(api_key=anthropic_api_key)

    messages_claude = [
        {
            "role": "user",
            "content": [{"type": "text", "text": "Perform the prompt"}]
        }
    ]

    if continue_response:
        messages_claude.append({
            "role": "assistant",
            "content": [{"type": "text", "text": previous_messages}]
        })
        messages_claude.append({
            "role": "user",
            "content": [{"type": "text", "text": "Continue where you stopped from"}]
        })

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8192,
        temperature=temperature,
        system=prompt,
        messages=messages_claude
    )

    return f"{previous_messages} {response.content[0]['text']}" if continue_response else response.content[0].text


