import os
import requests
from typing import Tuple, List

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MAPBOX_BASE_URL = "https://api.mapbox.com/directions-matrix/v1/mapbox/driving"


def get_matrix_distance(coords: List[Tuple[float, float]]) -> List[List[float]]:
    """
    Appelle Mapbox Matrix pour obtenir la matrice des distances (en mètres) entre tous les points fournis.
    :param coords: Liste de tuples (lon, lat)
    :return: matrice des distances en mètres
    """
    if not MAPBOX_TOKEN:
        raise RuntimeError("MAPBOX_TOKEN n'est pas défini dans l'environnement.")
    # Format Mapbox : lon,lat;lon,lat;...
    coord_str = ";".join([f"{lon},{lat}" for lon, lat in coords])
    url = f"{MAPBOX_BASE_URL}/{coord_str}"
    params = {
        "access_token": MAPBOX_TOKEN,
        "annotations": "distance,duration"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["distances"]  # distances en mètres


def match_passenger_mapbox(
    driver_start: Tuple[float, float],
    driver_end: Tuple[float, float],
    passenger_start: Tuple[float, float],
    passenger_end: Tuple[float, float],
    max_extra_km: float = 5.0
) -> bool:
    """
    Vérifie si un conducteur peut prendre un passager sans détour > max_extra_km
    :return: True si match, False sinon
    """
    # Ordre : driver_start, driver_end, passenger_start, passenger_end
    coords = [driver_start, driver_end, passenger_start, passenger_end]
    distances = get_matrix_distance(coords)
    # Distance conducteur seul : driver_start ➔ driver_end
    normal_distance = distances[0][1] / 1000  # en km
    # Distance avec détour : driver_start ➔ passenger_start ➔ passenger_end ➔ driver_end
    detour_distance = (
        distances[0][2] + distances[2][3] + distances[3][1]
    ) / 1000  # en km
    extra_km = detour_distance - normal_distance
    print(f"Trajet normal: {normal_distance:.2f} km")
    print(f"Trajet avec détour: {detour_distance:.2f} km")
    print(f"Détour: {extra_km:.2f} km")
    return extra_km <= max_extra_km


if __name__ == "__main__":
    print("--- Exemple Mapbox Matrix : Andorre-la-Vieille centre ---")
    driver_start = (1.521, 42.507)   # Andorre-la-Vieille centre
    driver_end = (1.528, 42.513)     # Quartier nord
    passenger_start = (1.523, 42.509) # Quartier est
    passenger_end = (1.524, 42.510)   # Quartier est
    is_match = match_passenger_mapbox(driver_start, driver_end, passenger_start, passenger_end, max_extra_km=2.0)
    print("Match!" if is_match else "Pas de match.")

    print("\n--- Exemple Mapbox Matrix : détour raisonnable ---")
    driver_start = (1.521, 42.507)
    driver_end = (1.528, 42.513)
    passenger_start = (1.45, 42.45)
    passenger_end = (1.45, 42.45)
    is_match = match_passenger_mapbox(driver_start, driver_end, passenger_start, passenger_end, max_extra_km=3.0)
    print("Match Sud-Ouest!" if is_match else "Pas de match Sud-Ouest.")

    print("\n--- Exemple Mapbox Matrix : détour trop grand ---")
    passenger_start = (1.6, 42.6)
    passenger_end = (1.6, 42.6)
    is_match = match_passenger_mapbox(driver_start, driver_end, passenger_start, passenger_end, max_extra_km=1.0)
    if is_match:
        print("Match Nord-Est!")
    else:
        print(f"Désolé, le détour pour récupérer ce passager au Nord-Est dépasse 1 km. Pas de match.")
