import os
import requests

def get_matrix_distance(coord1, coord2, token=None):
    """Retourne la distance (en km) entre deux points avec Mapbox Matrix API."""
    if token is None:
        token = os.environ.get("MAPBOX_TOKEN")
    url = f"https://api.mapbox.com/directions-matrix/v1/mapbox/driving/{coord1[0]},{coord1[1]};{coord2[0]},{coord2[1]}?access_token={token}&annotations=distance"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    # distances[0][1] = distance entre point 1 et 2 en mètres
    return data['distances'][0][1] / 1000

def match_passenger_mapbox(driver_start, driver_end, passenger_start, passenger_end, max_extra_km=3.0, token=None):
    """
    Retourne True si le détour pour récupérer le passager est raisonnable (Mapbox Matrix API).
    """
    dist_normal = get_matrix_distance(driver_start, driver_end, token=token)
    # Trajet avec détour : conducteur va chercher passager puis va à l'arrivée
    dist_detour = get_matrix_distance(driver_start, passenger_start, token=token) + get_matrix_distance(passenger_start, driver_end, token=token)
    extra_km = dist_detour - dist_normal
    return extra_km <= max_extra_km
