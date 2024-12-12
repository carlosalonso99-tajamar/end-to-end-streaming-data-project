import threading
import time
import json
import socket
import logging
import os
from dotenv import load_dotenv

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # Enviar logs a stdout
    ]
)

# Cargar las variables del archivo .env
load_dotenv()

# Configuración del servidor
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 65432))

# Directorio de trayectos
TRAYECTO_DIR = os.getenv("TRAYECTO_DIR", "data")

# Diccionario para gestionar trayectos activos
active_cars = {}
lock = threading.Lock()  # Lock para gestionar acceso concurrente al diccionario


def handle_client(conn, addr):
    logging.info(f"Conexión establecida con {addr}")
    car_id = None  # Inicializar car_id para evitar errores de referencia no asignada
    try:
        # Recibir el trayecto seleccionado
        data = conn.recv(1024).decode('utf-8').strip()
        logging.info(f"Datos recibidos del cliente: {data}")
        request = json.loads(data)
        trayecto = request.get("trayecto")
        logging.info(f"Trayecto seleccionado: {trayecto}")

        # Mapa de trayectos a archivos JSON
        trayecto_files = {
            "Trayecto 1": f"{TRAYECTO_DIR}/trayecto1.json",
            "Trayecto 2": f"{TRAYECTO_DIR}/trayecto2.json",
            "Trayecto 3": f"{TRAYECTO_DIR}/trayecto3.json"
        }

        if trayecto not in trayecto_files:
            logging.error(f"Trayecto no válido: {trayecto}")
            conn.sendall(json.dumps({"error": "Trayecto no válido"}).encode('utf-8'))
            return

        # Cargar los datos del trayecto seleccionado
        try:
            with open(trayecto_files[trayecto], 'r') as f:
                car_data = json.load(f)
            logging.info(f"Datos cargados del JSON: {trayecto_files[trayecto]}")
        except FileNotFoundError:
            logging.error(f"Archivo no encontrado: {trayecto_files[trayecto]}")
            conn.sendall(json.dumps({"error": "Archivo de trayecto no encontrado"}).encode('utf-8'))
            return
        except json.JSONDecodeError:
            logging.error(f"Error al decodificar JSON: {trayecto_files[trayecto]}")
            conn.sendall(json.dumps({"error": "Archivo JSON no válido"}).encode('utf-8'))
            return

        # Extraer el `car_id` del primer registro
        if not car_data or not isinstance(car_data, list):
            conn.sendall(json.dumps({"error": "Formato del JSON no válido"}).encode('utf-8'))
            return

        car_id = car_data[0].get("car_id")
        logging.info(f"Car ID extraído: {car_id}")

        if not car_id:
            conn.sendall(json.dumps({"error": "No se encontró car_id en los datos"}).encode('utf-8'))
            return

        # Validar que el coche no tenga un trayecto activo
        with lock:
            if car_id in active_cars:
                logging.warning(f"Coche {car_id} ya tiene un trayecto activo.")
                conn.sendall(json.dumps({"error": f"Coche {car_id} ya tiene un trayecto activo"}).encode('utf-8'))
                return
            else:
                active_cars[car_id] = True  # Marcar el coche como activo

        # Transmitir los datos al cliente
        for data in car_data:
            conn.sendall(json.dumps(data).encode('utf-8'))
            time.sleep(1)

        logging.info(f"Trayecto completado para el coche {car_id}")
    except Exception as e:
        logging.error(f"Error gestionando el cliente {addr}: {e}")
    finally:
        conn.close()
        if car_id:
            with lock:
                active_cars.pop(car_id, None)
                logging.info(f"Car ID {car_id} liberado.")


def start_server():
    """Inicia el servidor y gestiona múltiples conexiones."""
    logging.info(f"Verificando existencia del directorio de trayectos: {TRAYECTO_DIR}")
    if not os.path.exists(TRAYECTO_DIR):
        logging.error(f"Directorio de trayectos no encontrado: {TRAYECTO_DIR}")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        logging.info(f"Servidor escuchando en {HOST}:{PORT}")
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    logging.info("Iniciando servidor...")
    start_server()
