import requests
import json
import random
from datetime import timedelta
from geopy.distance import geodesic

# Obtener la ruta desde Azure Maps
def get_route_from_azure_maps(api_key, start_lat, start_lon, end_lat, end_lon):
    url = f"https://atlas.microsoft.com/route/directions/json"
    params = {
        "api-version": "1.0",
        "subscription-key": api_key,
        "query": f"{start_lat},{start_lon}:{end_lat},{end_lon}",
        "travelMode": "car",
        "routeAttributes": "all"  # Solicitar todos los detalles
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "routes" in data:
            # Extraer los puntos de la ruta
            route_points = data["routes"][0]["legs"][0]["points"]
            return [{"latitude": point["latitude"], "longitude": point["longitude"]} for point in route_points]
        else:
            print("No se encontraron rutas.")
    else:
        print(f"Error al conectar con la API de Azure Maps: {response.status_code}")
    return []

# Generador de datos de ruta usando Azure Maps
def generate_taxi_route(api_key, start_lat, start_lon, end_lat, end_lon, car_id=None):
    if car_id is None:
        car_id = f"CAR-{random.randint(1000, 9999)}"

    # Obtener la ruta desde Azure Maps
    route_points = get_route_from_azure_maps(api_key, start_lat, start_lon, end_lat, end_lon)

    if not route_points:
        print("No se pudo obtener una ruta válida.")
        return []

    route = []
    elevation = random.uniform(50, 150)  # Elevación inicial en metros
    current_time = timedelta()  # Inicia en 00:00:00

    for i, point in enumerate(route_points):
        lat = point["latitude"]
        lon = point["longitude"]

        # Calcular distancia, velocidad y tiempo de viaje
        if i > 0:
            prev_lat, prev_lon = route_points[i - 1]["latitude"], route_points[i - 1]["longitude"]
            distance_km = geodesic((prev_lat, prev_lon), (lat, lon)).km
            
        # Incrementar tiempo en 1 segundo
            current_time += timedelta(seconds=1)

        else:
            distance_km = 0
            travel_time_seconds = 0

        # Actualizar elevación y tiempo
        elevation += random.uniform(-1, 1)  # Simular cambios en la elevación
        current_time += timedelta(seconds=travel_time_seconds)

        # Agregar punto a la ruta
        route.append({
            "car_id": car_id,
            "latitude": lat,
            "longitude": lon,
            "elevation": round(elevation, 2),
            "timestamp": str(current_time),
            "distance_km": round(distance_km, 3),
        })

    return route

# Configurar punto de inicio y fin
start_lat = 40.397667314975536  # Latitud de inicio
start_lon = -3.6496011457469146  # Longitud de inicio
end_lat = 40.490252679705584  # Latitud de destino
end_lon = -3.650522047596679  # Longitud de destino
car_id = "VIKUNETA"

# Reemplaza con tu clave de API de Azure Maps
api_key = "h9RZCBvt0gpRLDbfnDUPH36HZSiyoyXK5EHcAOhrazt04xi4qfMJJQQJ99ALACi5YpzfWOEbAAAgAZMP2Xph"

# Generar ruta de taxi
route = generate_taxi_route(api_key, start_lat, start_lon, end_lat, end_lon, car_id=car_id)

# Mostrar resultados
if route:
    print(f"Ruta generada para el coche {car_id}:")
    for point in route:
        print(point)

    # Guardar los datos en un archivo JSON
    json_file = "azure_taxi_route_data.json"
    with open(json_file, mode='w', encoding='utf-8') as file:
        json.dump(route, file, indent=4)

    print(f"\nLos datos de la ruta del taxi se han guardado en el archivo {json_file}.")