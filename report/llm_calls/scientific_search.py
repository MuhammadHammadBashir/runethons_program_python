# from dotenv import load_dotenv
# import os
# from openai import OpenAI
# load_dotenv()

# client = OpenAI(api_key=os.getenv("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")
# # chat completion without streaming

# def scientific_search(research_prompt):
#     messages = [
#         {
#             "role": "system",
#             "content": (
#     """
#     you are the intelligent scrape who finds the paper bibliography and provides the summary of that paper  
#     """
#             ),
#         },
#         {   
#             "role": "user",
#             "content": (
#             research_prompt
#             ),
#         },
#     ]

#     response = client.chat.completions.create(
#         model="sonar-pro",
#         messages=messages,
#     )

#     return response.choices[0].message.content


from dotenv import load_dotenv
import os
load_dotenv()

import anthropic
import json
import re


import google.generativeai as genai




gemini_api_key = os.getenv("GEMINI_API_KEY")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
# chat completion without streaming



from pydantic import BaseModel, HttpUrl
from typing import List, Optional,Union

class BibliographyEntry(BaseModel):
    title: str
    authors: List[str]
    year: int
    source: str
    doi: Optional[Union[HttpUrl, str]]  # Ensures doi is either a valid URL or None

class ResearchOutput(BaseModel):
    research_summary: str
    bibliography: List[BibliographyEntry]





def scientific_search(research_prompt,model="claude"):

    if model == 'claude':
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            system="You are an expert research assistant. Only return valid JSON as instructed.",
            messages=[
                {"role": "user", "content": research_prompt}
            ]
        )
        if not response or not response.content:
            raise ValueError("Error: Empty response from model.")

        json_text = response.content[0].text
    if model == 'gemini':
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
        response = model.generate_content(research_prompt)
        if not response or not response.text:
            raise ValueError("Error: Empty response from model.")

        json_text = response.text
        




    # Remove unwanted formatting (like ```json ... ```)
    json_text = re.sub(r"```json\s*|\s*```", "", json_text).strip()

    try:
        structured_output = json.loads(json_text)

        # Ensure DOI is None if missing or invalid
        for entry in structured_output.get("bibliography", []):
            if entry.get("doi") in ["N/A", "null", ""]:
                entry["doi"] = None

        # Validate JSON with Pydantic
        search_results = ResearchOutput(**structured_output)
        return search_results  # This will now be a validated Pydantic object

    except json.JSONDecodeError:
        raise ValueError("Error: Model returned invalid JSON.")
    except Exception as e:
        raise ValueError(f"Error parsing LLM response: {e}")
