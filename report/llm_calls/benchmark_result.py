from dotenv import load_dotenv
import os
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# chat completion without streaming
def benchmark_result(research_prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a research assistant that will benchmark results to support my work."
        },
        {   
            "role": "user",
            "content": research_prompt
        },
    ]

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        messages=messages,
    )

    return response.content[0].text
