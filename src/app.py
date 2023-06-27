from flask import Flask
import requests
import json

app = Flask(__name__)

def obtener_datos_productos():
    url_endpoint = "http://177.222.127.82/bambamws/api/productos/obtenerproductos"  # Reemplaza con la URL real del endpoint
    response = requests.get(url_endpoint)
    if response.status_code == 200:
        datos_productos = response.json()
        return datos_productos
    else:
        # Manejo de errores en caso de que la solicitud falle
        return None

def notificarStockBajo():
    datos_productos = obtener_datos_productos()
    for producto in datos_productos['productos']:
            proStock = producto['proStock']
            umbral = 10  # Umbral mínimo para enviar notificaciones (valor estático)
            
            if proStock < umbral:
                print(f"El stock del producto {producto['proNombre']} está por debajo del umbral.")
                # Aquí puedes agregar la lógica para enviar la notificación, como enviar un correo electrónico o llamar a una función específica.

@app.route('/')
def hello():
    notificarStockBajo()
    return '¡Hola, Flask!'

if __name__ == '__main__':
    app.run()
