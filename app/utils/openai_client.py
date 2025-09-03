from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_EMBED_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def chat(messages, model: str = OPENAI_MODEL):
    return client.chat.completions.create(model=model, messages=messages)

def embed(texts, model: str = OPENAI_EMBED_MODEL):
    return client.embeddings.create(model=model, input=texts)
