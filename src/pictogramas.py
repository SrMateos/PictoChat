'''
genérame un backend que reciba un texto y use langchain 
y ollama para parsear las ideas más importantes
Tras esto, genérame un pictograma con las ideas más importantes
usando la api de https://arasaac.org/developers/api
'''

from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
import requests

app = Flask(__name__)
llm = Ollama(model="llama2")

prompt = '''
Identify key concepts within the text enclosed by {}. Keep the summary concise and in Spanish.
Provide output in JSON format.The JSON format should be as follows: {"idea1": "Idea 1"}
Provide just one idea.

Example:
Input: "Tengo dolor de estómago"
Output: { "idea1": "Dolor de Estómago" }
'''


def llm_get_main_ideas(text):
    return llm.invoke(text)

def get_pictogram(text):
    url = f"https://api.arasaac.org/api/pictograms/es/search/{text}"
    response = requests.get(url)
    data = response.json()
    if len(data) > 0:
        return data[0]['_id']
    return None

@app.route('/pictogramas', methods=['POST'])
def pictogramas():
    data = request.get_json()
    text = data['text']
    main_ideas = llm_get_main_ideas(text)
    pictograms = []
    for idea in main_ideas:
        pictograms.append(get_pictogram(idea))
    return jsonify(pictograms)

if __name__ == '__main__':
    your_text = "Me duele muchísimo la cabeza desde ayer"
    formated_prompt = str(prompt.replace('{}', f'\"{your_text}\"'))
    print(llm.invoke(formated_prompt))