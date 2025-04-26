import base64
import requests
import json

# server:
# OLLAMA_API_URL_MULTI = "http://172.16.61.73:11434/api/generate"

# Endpoint locale di Ollama
OLLAMA_API_URL_MULTI = "http://172.16.61.73:11434/api/generate"
OLLAMA_API_URL = "http://172.16.61.73:11434/api/generate"


# Funzione per inferenza streaming LLM testuale
def ask_ollama_stream(OLLAMA_API_URL, user_prompt, system, temp, model):
    payload = {
        "model": model,
        "system": system,
        "prompt": user_prompt,
        "stream": True,
        "temperature": temp,
        "top_k": 0,
    }
    risposta = ""
    try:
        with requests.post(OLLAMA_API_URL, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        token_json = json.loads(line.decode('utf-8'))
                        token = token_json.get("response", "")
                        print(token, end="", flush=True)
                        risposta += token
                    except json.JSONDecodeError as e:
                        print(f"\n[Errore parsing token JSON]: {e}")
            print()  # newline finale
    except requests.exceptions.RequestException as e:
        print(f"Errore nella richiesta: {e}")
    return risposta


# Funzione per convertire immagine in base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


# Funzione per inferenza multimodale su immagine
def describe_image(OLLAMA_API_URL_MULTI, image_path, prompt, temp, model):
    image_base64 = image_to_base64(image_path)
    data = {
        "model": model,
        "prompt": prompt,
        "images": [image_base64],
        "temperature": temp,
        "stream": False,
        "top_k": 0,
    }
    try:
        response = requests.post(OLLAMA_API_URL_MULTI, json=data)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Nessuna risposta dal modello.")
        else:
            return f"Errore: {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Errore: impossibile connettersi a Ollama."
