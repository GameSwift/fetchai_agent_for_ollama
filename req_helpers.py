import requests

def request_ollama(prompt, model, host):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'{{"model": "{model}", "prompt": "{prompt}", "stream": false}}'
    response = requests.post(
        f'"{host}"', 
        headers=headers, 
        data=data
        )

    return response.json()