from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.perplexity.ai")
# chat completion without streaming

def benchmark_result(research_prompt):
    messages = [
        {
            "role": "system",
            "content": (
    """
    You are research assistant that will benchmark results to support my work
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
        model="gpt-4o",
        messages=messages,
    )

    return response.choices[0].message.content