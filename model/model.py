from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.genai import types
import base64
client = genai.Client()

def get_gemini_response(input,pdf_content,prompt):
    image_parts = [
        types.Part.from_bytes(
            data=base64.b64decode(page["data"]),
            mime_type=page["mime_type"]
        )
        for page in pdf_content
    ]
    contents = [
        prompt,                        
        f"Job Description:\n{input}",  
        *image_parts                   
    ]
    response = client.models.generate_content(
         model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)  # disable ‘slow thinking’
        ),
    )
    return response.text
