from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

client = OpenAI(api_key=os.getenv("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")
# chat completion without streaming

def scientific_search(research_prompt):
    messages = [
        {
            "role": "system",
            "content": (
    """
    you are the intelligent scrape who finds the paper bibliography and provides the summary of that paper  
    """
            ),
        },
        {   
            "role": "user",
            "content": (
            research_prompt
            ),
        },
    ]

    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )

    return response.choices[0].message.content