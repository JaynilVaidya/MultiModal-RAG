#%%
import faiss
from sentence_transformers import SentenceTransformer
from together import Together
import os
from dotenv import load_dotenv 
from helper import get_simcontext   

#%% rag chain

index = faiss.read_index("my_faiss_index.index")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
load_dotenv()

Question = """
Nodes in a graph database can possess multiple relationships, allowing for versatile and interconnected data modeling without compromising performance.

- True
- False

    """
simcontext = get_simcontext([Question], embedding_model, index)
joinedContext = "\n".join(simcontext)

API_KEY = os.getenv("TOGETHER_API_KEY") # Get your API key from https://together.api.jina.ai
client = Together(api_key=API_KEY)

system_prompt = "Only use the information from the provided context to answer the Query. The input will always be text-based. Always keep your answers concise and to the point. Never exceed 500 tokens in your response. If the context does not provide enough information, respond with 'Insufficient information.'"

response = client.chat.completions.create(
    model="meta-llama/Llama-Vision-Free",
    messages=[{"role":"system", "content": system_prompt, "role": "user", "content": f"Context: {joinedContext} \n Query: {Question}"}],
)

print(response.choices[0].message.content)