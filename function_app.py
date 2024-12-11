import logging
import requests
import azure.functions as func
from azure.eventhub import EventHubProducerClient, EventData
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Variables de entorno
API_URL = os.getenv("API_URL")
EVENT_HUB_CONNECTION_STRING = os.getenv("EVENT_HUB_CONNECTION_STRING")
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME")

app = func.FunctionApp()

@app.timer_trigger(schedule="*/1 * * * * *", arg_name="myTimer", run_on_startup=False,
                    use_monitor=False)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    try:
        # Hacer una solicitud GET a la API
        response = requests.get(API_URL)

        # Comprobar si la respuesta fue exitosa
        if response.status_code == 200:
            # Datos del estado del coche
            car_state = response.json()
            logging.info(f"Data received: {car_state}")
            
            # Enviar datos al Event Hub
            send_to_event_hub(car_state)

        elif response.status_code == 404:
            logging.warning("No more data available from the API.")
        else:
            logging.error(f"API returned an error. Status Code: {response.status_code}, Message: {response.text}")
    except requests.exceptions.RequestException as e:
        # Manejo de errores de red o conexión
        logging.error(f"Error connecting to API: {e}")

    logging.info('Python timer trigger function executed.')

def send_to_event_hub(data: dict):
    """
    Enviar datos al Event Hub.
    """
    try:
        producer = EventHubProducerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STRING,
            eventhub_name=EVENT_HUB_NAME
        )
        with producer:
            # Crear un lote de eventos
            event_data_batch = producer.create_batch()
            # Añadir el evento (convertir a cadena JSON)
            event_data_batch.add(EventData(str(data)))
            # Enviar el lote
            producer.send_batch(event_data_batch)
            logging.info("Data sent to Event Hub successfully.")
    except Exception as e:
        logging.error(f"Error sending data to Event Hub: {e}")
