
import requests


def chat(messages):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.1:8B",
            "messages": messages,
            "stream": False
        }
        
    )
    if response.status_code == 200:
        return response.json()["message"]["content"]
    else:
        raise Exception(f"Ollama error: {response.text}")
