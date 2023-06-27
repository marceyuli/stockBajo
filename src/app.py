from flask import Flask
import requests
import json
import smtplib 
from email.mime.text import MIMEText
app = Flask(__name__)

def enviar_notificacion_por_correo(producto_nombre):
    # Configura los detalles del servidor de correo y las credenciales de autenticación
    servidor_smtp = "smtp-relay.sendinblue.com"
    puerto_smtp = 587
    usuario_smtp = "yulianamarcela200@gmail.com"
    contrasena_smtp = "rFAjnUHaVDXZzMI6"

    remitente = "bambamAdmin@gmail.com"
    destinatario = "yulianamarcela200@gmail.com"
    asunto = "Stock bajo de producto"
    mensaje = f"El stock del producto {producto_nombre} está por debajo del stock minimo, tomar previsiones. "

    # Crea el objeto MIMEText con el contenido del mensaje
    mensaje_mime = MIMEText(mensaje)
    mensaje_mime["From"] = remitente
    mensaje_mime["To"] = destinatario
    mensaje_mime["Subject"] = asunto

    try:
        # Conecta y autentica con el servidor SMTP
        servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
        servidor.starttls()
        servidor.login(usuario_smtp, contrasena_smtp)

        # Envía el correo electrónico
        servidor.send_message(mensaje_mime)

        # Cierra la conexión con el servidor SMTP
        servidor.quit()

        print("Notificación enviada por correo electrónico")
    except Exception as e:
        print("Error al enviar la notificación por correo electrónico:", str(e))

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
                enviar_notificacion_por_correo(producto['proNombre'])
                # Aquí puedes agregar la lógica para enviar la notificación, como enviar un correo electrónico o llamar a una función específica.

@app.route('/')
def hello():
    notificarStockBajo()
    return 'Microservicio de notificaciones Bambam'

if __name__ == '__main__':
    app.run()
