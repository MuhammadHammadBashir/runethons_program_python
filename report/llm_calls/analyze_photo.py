import anthropic
from dotenv import load_dotenv
import os

load_dotenv()


client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
def analyze_photo(base64_image,frame_number,VISION_PROMPT):
    response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": VISION_PROMPT
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ]
        )


    description = response.content[0].text  # Extract text properly
    
    return frame_number,description
