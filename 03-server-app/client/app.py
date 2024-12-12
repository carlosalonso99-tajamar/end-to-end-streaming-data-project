import logging
from flask import Flask, render_template, request, jsonify
import socket
import json
import os
from dotenv import load_dotenv
from azure.eventhub import EventHubProducerClient, EventData

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Cargar variables de entorno
load_dotenv()

# Configuración de Event Hub
EVENT_HUB_CONNECTION_STRING = os.getenv("EVENT_HUB_CONNECTION_STRING")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")
if not EVENT_HUB_CONNECTION_STRING or not EVENT_HUB_NAME:
    logging.critical("Las variables EVENT_HUB_CONNECTION_STRING y EVENT_HUB_NAME son obligatorias.")
    exit(1)

# Configuración del servidor de datos
SERVER_HOST = os.getenv("HOST")
SERVER_PORT = os.getenv("PORT")
if not SERVER_HOST or not SERVER_PORT:
    logging.critical("Las variables HOST y PORT son obligatorias.")
    exit(1)

SERVER_PORT = int(SERVER_PORT)

# Inicializar Flask
app = Flask(__name__)

# Crear una única instancia del cliente de Event Hub
producer = EventHubProducerClient.from_connection_string(
    conn_str=EVENT_HUB_CONNECTION_STRING,
    eventhub_name=EVENT_HUB_NAME
)

# Función para enviar datos a Event Hub
def send_to_event_hub(data, retries=3):
    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Intentando enviar datos a Event Hub (intento {attempt}/{retries})...")
            # Obtener el car_id como partition_key
            partition_key = data.get("car_id")
            if not partition_key:
                raise ValueError("El campo 'car_id' es obligatorio para la partition_key")

            # Crear el evento con los datos
            event_data = EventData(json.dumps(data))
            producer.send_batch([event_data], partition_key=partition_key)
            logging.info(f"Datos enviados a Event Hub con partition_key '{partition_key}': {data}")
            return  # Salir del bucle si el envío fue exitoso

        except Exception as e:
            logging.error(f"Error enviando datos a Event Hub (intento {attempt}/{retries}): {e}")
            if attempt == retries:
                logging.critical("Se agotaron los reintentos. Los datos no pudieron enviarse.")
                raise



# Ruta principal
@app.route('/')
def index():
    logging.info("Accediendo a la página principal")
    return render_template('index.html')

# Ruta para iniciar trayecto
@app.route('/start', methods=['POST'])
def start_trayecto():
    data = request.json
    trayecto = data.get('trayecto')
    if not trayecto:
        logging.error("No se proporcionó el campo 'trayecto' en la solicitud.")
        return jsonify({"error": "El campo 'trayecto' es obligatorio"}), 400

    logging.info(f"Inicio del trayecto recibido: {trayecto}")
    try:
        logging.info(f"Conectando al servidor de datos en {SERVER_HOST}:{SERVER_PORT}...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            logging.info(f"Conexión establecida con el servidor de datos.")

            request_data = json.dumps({"trayecto": trayecto})
            client_socket.sendall(request_data.encode('utf-8'))
            logging.info(f"Datos del trayecto enviados al servidor: {request_data}")

            while True:
                response = client_socket.recv(1024)
                if not response:
                    logging.info("No se recibieron más datos del servidor. Finalizando conexión.")
                    break
                response_data = json.loads(response.decode('utf-8'))
                logging.info(f"Datos recibidos del servidor: {response_data}")
                send_to_event_hub(response_data)

            return jsonify({"message": f"Datos del trayecto '{trayecto}' enviados a Event Hub"})
    except Exception as e:
        logging.error(f"Error procesando el trayecto: {e}")
        return jsonify({"error": str(e)}), 500

# Cerrar el cliente de Event Hub al finalizar
@app.teardown_appcontext
def close_eventhub_client(exception=None):
    if producer:
        logging.info("Cerrando cliente de Event Hub...")
        producer.close()

# Ejecutar Flask
if __name__ == '__main__':
    logging.info("Iniciando la aplicación Flask...")
    app.run(host='0.0.0.0', port=5000)
