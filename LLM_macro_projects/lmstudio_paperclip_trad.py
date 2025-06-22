import requests
import pyperclip
import json



def catch_texte_to_analyse():

    # Get the content of the clipboard
    clipboard_content = pyperclip.paste()

    return clipboard_content



def release_text_translated(traduction):
    pyperclip.copy(traduction)
    


def LLM_traduction (text_to_translate):
    url = "http://localhost:1234/v1/chat/completions"
    headers = {
        "Authorization": "Bearer lm-studio",
        "Content-Type": "application/json"
    }
    data = {
        "model": "granite-3.2-8b-instruct",
        "messages": [
            {"role": "user", "content": """
                    
                        # Tâche
                        Analyse le texte ci-dessous et fournis moi une traduction en anglais dans réponse strictement au format JSON.

                        ## Texte à analyser
                        """+ text_to_translate +"""

                        ## Contraintes
                        - Répond uniquement avec un objet JSON, sans texte autour.
                        - Le JSON doit contenir les clés suivantes :
                        - `traduction`: "insert traduction here"
                      
                        ## Format attendu
                        ''' json
                        {
                        "traduction": "..",
                        
                        }
            """}
        ],
        "temperature": 0.0
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']


clipboard = catch_texte_to_analyse()
print(clipboard)
trad_brute_brute = LLM_traduction(clipboard)
print(trad_brute_brute)
trad_brute = json.load(trad_brute_brute)
trad = json.load(trad_brute)


print(trad["traduction"])
#release_text_translated(trad)