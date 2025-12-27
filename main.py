from together import Together
import os

client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

def chat(messages):
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
        messages=messages,
        max_tokens=200,
    )
    return response.choices[0].message.content
