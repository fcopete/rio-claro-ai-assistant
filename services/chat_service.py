from openai import OpenAI
from config import AZURE_OPENAI_ENDPOINT,AZURE_OPENAI_API_KEY,AZURE_OPENAI_DEPLOYMENT,MAX_CHAT_RESPONSE_TOKENS,CHAT_TEMPERATURE
client=OpenAI(base_url=AZURE_OPENAI_ENDPOINT,api_key=AZURE_OPENAI_API_KEY)
SYSTEM_PROMPT="Eres Rio Claro AI Assistant"
def ask_chatbot(question, history=None):
    messages=[{"role":"system","content":SYSTEM_PROMPT}]
    if history and isinstance(history,list): messages.extend(history)
    messages.append({"role":"user","content":question})
    r=client.chat.completions.create(model=AZURE_OPENAI_DEPLOYMENT,messages=messages,temperature=CHAT_TEMPERATURE,max_tokens=MAX_CHAT_RESPONSE_TOKENS)
    return r.choices[0].message.content
def test_connection():
    ask_chatbot("test")
    return True
