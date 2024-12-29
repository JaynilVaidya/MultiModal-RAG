from together import Together
from PIL import Image
import base64
import json
import PyPDF2
from together import Together
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY") # Get your API key from https://together.api.jina.ai
client = Together(api_key=API_KEY)


def get_simcontext(Question, embedding_model, index):
    query_vector = embedding_model.encode(Question, convert_to_numpy=True, show_progress_bar=True)
    distances, indices = index.search(query_vector, 5)
    print(distances, indices)

    simcontext = []

    with open('metadata.json', 'r', encoding='utf-8') as file:
        metadata = json.load(file)

    for i in indices[0]:
        simcontext.append(metadata["corpus"][str(i)]["content"])
        
    return simcontext

def interpret_image_with_context(base64_images, system_prompt, context):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"Context: {context}"},
            ],
        },
        {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
    ]
    
    for base64_image in base64_images:
        messages[0]["content"].append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}",
                },
            }
        )
    
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",
        messages=messages
    )
    
    ans = response.choices[0].message.content
    
    return ans
