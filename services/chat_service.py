from openai import AzureOpenAI
from config import AZURE_OPENAI_ENDPOINT,AZURE_OPENAI_API_KEY,AZURE_OPENAI_API_VERSION,AZURE_OPENAI_DEPLOYMENT
client=AzureOpenAI(api_key=AZURE_OPENAI_API_KEY,api_version=AZURE_OPENAI_API_VERSION,azure_endpoint=AZURE_OPENAI_ENDPOINT)
SYSTEM_PROMPT="You are Rio Claro assistant."

def ask_chatbot(question,history=None):
    messages=[{"role":"system","content":SYSTEM_PROMPT}]
    if history: messages.extend(history)
    messages.append({"role":"user","content":question})
    r=client.chat.completions.create(model=AZURE_OPENAI_DEPLOYMENT,messages=messages)
    return r.choices[0].message.content

def test_connection():
    client.chat.completions.create(model=AZURE_OPENAI_DEPLOYMENT,messages=[{"role":"user","content":"test"}],max_tokens=3)
    return True
