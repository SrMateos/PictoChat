import re
from nltk.tokenize import word_tokenize

# Descargar recursos adicionales de NLTK
#nltk.download('punkt')

# Expresiones regulares para detectar zonas del cuerpo
patrones_zonas_cuerpo = {
    "cabeza": r'\b(cabeza|cabezas)\b',
    "torso": r'\b(tórax|pecho|abdomen)\b',
    "estómago": r'\b(estómago|estómagos|barriga)\b',
    "brazo": r'\b(brazo|brazos)\b',
    "pierna": r'\b(pierna|piernas)\b',
    "espalda": r'\b(espalda|espalda)\b',
    "cuello": r'\b(cuello|cuellos)\b',
    "cadera": r'\b(cadera|caderas)\b',
    "mano": r'\b(mano|manos)\b',
    "pie": r'\b(pie|pies)\b',
    "muñeca": r'\b(muñeca|muñecas)\b',
    "tobillo": r'\b(tobillo|tobillos)\b',
    "codo": r'\b(codo|codos)\b',
    "rodilla": r'\b(rodilla|rodillas)\b',
    "hombro": r'\b(hombro|hombros)\b', 
    # Puedes añadir más patrones según tus necesidades
}

patrones_dolencias = { 
    "dolor": r'\b(dolor|dolores|duele|dolido|molestia|molestias|molestado|calambre|calambres|molesta)\b',
    "hinchazón": r'\b(hinchazón|hinchazones|hinchado)\b',
    "sangrado": r'\b(sangrado|sangrados|sangra|sangran)\b',
    "picor": r'\b(picor|picor|pican|pica|picado)\b',
    "rigidez": r'\b(rigidez|rigideces|rígido|duro)\b',
    "calor": r'\b(calor|calores)\b',
    "frío": r'\b(frío|fríos)\b',
    "fiebre": r'\b(fiebre|fiebres)\b',
    "tos": r'\b(tos|toses|tosido|tosidos)\b',
    "moco": r'\b(moco|mocos|moquea|moqueas|moqueado)\b',
    "vómito": r'\b(vómito|vómitos|vomita|vomitan|vomitado)\b',
    "mareado": r'\b(mareado|mareada|mareados|mareadas|mareo)\b',
    # Puedes añadir más patrones según tus necesidades
}

patrones_respuesta = {
    "sí": r'\b(sí|si|afirmativo)\b',
    "no": r'\b(no|negativo)\b',
    "no sé": r'\b(no sé|no lo sé|no se)\b',
    "no entiendo": r'\b(no entiendo|no comprendo)\b',
    "siempre" : r'\b(siempre)\b',
    "nunca" : r'\b(nunca)\b',
    "a veces" : r'\b(a veces)\b',
    "mucho" : r'\b(mucho)\b',
    "poco" : r'\b(poco)\b',
    "nada" : r'\b(nada)\b'
}

# Función para detectar la zona del cuerpo en una pregunta
def detectar_zona_cuerpo(tokens):
    for zona, patron in patrones_zonas_cuerpo.items():
        for token in tokens:
            if re.search(patron, token, re.IGNORECASE):
                return zona
    return None

# Función para detectar dolencias en una pregunta
def detectar_dolencia(tokens):
    for dolencia, patron in patrones_dolencias.items():
        for token in tokens:
            if re.search(patron, token, re.IGNORECASE):
                return dolencia
    return None

def detectar_respuesta(tokens):
    for respuesta, patron in patrones_respuesta.items():
        for token in tokens:
            if re.search(patron, token, re.IGNORECASE):
                return respuesta
    return None

# Función para procesar una pregunta y detectar la zona del cuerpo
def procesar_pregunta(pregunta):
    # Tokenizar la pregunta
    tokens = word_tokenize(pregunta)

    # Detectar zonas del cuerpo en los tokens
    zona_del_cuerpo = detectar_zona_cuerpo(tokens)
    dolencia = detectar_dolencia(tokens)

    return dolencia, zona_del_cuerpo

# Función para detectar la respuesta en una pregunta
def procesar_respuesta(respuesta):
    tokens = word_tokenize(respuesta)
    respuesta = detectar_respuesta(tokens)
    return respuesta

def get_tokens(entrada):
    entrada = entrada.lower()
    # Procesar la pregunta y detectar la zona del cuerpo
    dolencia, zona_del_cuerpo = procesar_pregunta(entrada)
    respuesta = procesar_respuesta(entrada)
    if respuesta is None:    
        respuesta = ""
    else:
        respuesta = respuesta + " "
    # Imprimir el resultado
    if zona_del_cuerpo is not None and dolencia is not None:
        return respuesta + dolencia + " de " + zona_del_cuerpo
    else:
        if dolencia is None:
            dolencia = ""
        if zona_del_cuerpo is None:
            zona_del_cuerpo = ""
        #if len(respuesta + dolencia)>0:
        #    zona_del_cuerpo = " " + zona_del_cuerpo
        return respuesta + dolencia + zona_del_cuerpo
