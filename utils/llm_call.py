import os
from dotenv import load_dotenv
from mistralai import Mistral
load_dotenv()
API_key=os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=API_key)
def call_llm(prompt):
    model="ministral-3b-2410"
    response=client.chat.complete(
                model=model,
                messages=[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            )
    return response.choices[0].message.content