import requests

def obtener_datos_api(api_url):
    response = requests.get(api_url)
    return response.json()