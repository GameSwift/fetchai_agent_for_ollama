import requests

def request_ollama(prompt):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'{{"model": "llama2", "prompt": "{prompt}", "stream": false}}'
    response = requests.post(
        'http://localhost:11434/api/generate', 
        headers=headers, 
        data=data
        )

    return response.json()