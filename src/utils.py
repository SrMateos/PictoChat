import requests
import json
import urllib.parse
import tokenizador

def procesar_texto(texto):
    try:
        palabras = texto.split()
        # URL de la API a la que enviarás el texto
        url_api1 = "https://api.arasaac.org/v1/pictograms/es/bestsearch/"
        url_api2 = "https://api.arasaac.org/v1/pictograms/{id}?download=false"
        
        ids = []
        print(texto.split())
        # Enviar la solicitud GET a la API con los datos
        for palabra in texto.split():
            response = requests.get(url_api1 + urllib.parse.quote(palabra))
            # print(response)

            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                # Extraer el texto de la respuesta
                texto_procesado = response.json()
                # print(type(texto_procesado), texto_procesado)          
                ids.append(texto_procesado[0]['_id'])
                # print(ids)
            else:
                # print("La solicitud no fue exitosa. Código de estado:", response.status_code)
                pass
        # print (ids)
        return [url_api2.format(id=id) for id in ids]
        
    
    except Exception as e:
        print("Ocurrió un error al procesar el texto:", str(e))
        return None


if __name__ == "__main__":
    texto = "Tengo hambre ahora"
    texto_procesado = procesar_texto(texto)
    if texto_procesado:
        print("Texto procesado:")
        for url in texto_procesado:
            print(url)
    else:
        print("No se pudo procesar el texto.")