from openai import OpenAI

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT
)

client = OpenAI(
    base_url=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY
)

SYSTEM_PROMPT = """
You are Rio Claro AI Assistant.
"""


def ask_chatbot(question):

    response = client.responses.create(

        model=
            AZURE_OPENAI_DEPLOYMENT,

        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.output_text


def test_connection():

    response = client.responses.create(

        model=
            AZURE_OPENAI_DEPLOYMENT,

        input="test"
    )

    return response.output_text