from azure.eventhub import EventHubProducerClient, EventData
import os
from dotenv import load_dotenv
load_dotenv()


connection_string = os.getenv("EVENT_HUB_CONNECTION_STRING")
eventhub_name = os.getenv("EVENT_HUB_NAME")

try:
    producer = EventHubProducerClient.from_connection_string(conn_str=connection_string, eventhub_name=eventhub_name)
    event_data = EventData("Test event")
    producer.send_batch([event_data])
    print("Mensaje enviado correctamente.")
except Exception as e:
    print(f"Error al conectar con Event Hub: {e}")
finally:
    producer.close()
