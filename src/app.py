
from flask import Flask, render_template, request
import utils

import json

import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Inicio', css="output.css")

@app.route('/guardar_respuestas', methods=['POST'])
def guardar_respuestas():
        
    idx = request.form.get('idx')

    with open('informe.json', 'r') as file:
        informe = json.load(file)
    
    bloque = informe[-1]
    bloque['respuestas'][int(idx)-1]['elegida'] = True

    with open('informe.json', 'w') as file:
        json.dump(informe, file, indent=4)
    
    return render_template('index.html', title='Inicio', css="output.css")

@app.route('/generar_informe', methods=['POST'])
def generar_informe():
    with open('informe.json', 'r') as file:
        informe = json.load(file)

    preguntas_con_respuesta = []
    for bloque in informe:
        pregunta = bloque["pregunta"][0]  # Obtener la pregunta (suponiendo que siempre es una lista con un solo elemento)
        respuestas = bloque["respuestas"]
    
        # Iterar sobre las respuestas para encontrar la respuesta elegida
        for respuesta in respuestas:
            if respuesta["elegida"]:
                # Si la respuesta está marcada como elegida, agregar la pregunta y la respuesta al resultado
                pregunta_con_respuesta = {
                    "pregunta": pregunta,
                    "respuesta_elegida": respuesta["texto"]
                }
                preguntas_con_respuesta.append(pregunta_con_respuesta)

    for pregunta_con_respuesta in preguntas_con_respuesta:
        print(pregunta_con_respuesta)

    return render_template('informe.html', preguntas_con_respuesta = preguntas_con_respuesta)

@app.route('/procesar', methods=['POST'])
def procesar():
    # Obtener las preguntas del formulario
    pregunta = request.form.getlist('pregunta[]')
    print("Pregunta:", pregunta)
    
    # Obtener las respuestas del formulario (solo las que no están vacías)
    respuestas = [respuesta for respuesta in request.form.getlist('respuesta[]') if respuesta]
    print("Respuestas:", respuestas)

    bloque_id = str(uuid.uuid4())

    bloque_pregunta_respuestas = {
        "id": bloque_id,
        "pregunta": pregunta,
        "respuestas": [
            {"texto": respuesta, "elegida": False} for respuesta in respuestas
        ]
    }
    try:
        with open('informe.json', 'r') as informe:
            informe_previo = json.load(informe)
    except:
        informe_previo = []
    
    informe_previo.append(bloque_pregunta_respuestas)
    with open('informe.json', 'w') as informe:
        json.dump(informe_previo, informe, indent=4)


    imagenes_pregunta = utils.procesar_texto(pregunta[0])
    print("URL de la imagen:", imagenes_pregunta)
    # Puedes redirigir a otra página aquí

    matriz_respuestas = [utils.procesar_texto(respuesta) for respuesta in respuestas]
    print("URL de las imágenes de las respuestas:", matriz_respuestas   )
    return render_template('preguntas.html', imagenes_pregunta=imagenes_pregunta, matriz_respuestas=matriz_respuestas, id=bloque_id, css="output.css")
 
if __name__ == '__main__':
    app.run(debug=True)
