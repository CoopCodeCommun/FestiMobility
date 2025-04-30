import requests
from typing import Tuple, List

VALHALLA_URL = "http://localhost:8002"


def get_route_distance(coords: List[Tuple[float, float]]) -> float:
    """
    Appelle Valhalla pour calculer la distance d'un trajet donné (en km)
    :param coords: Liste de tuples (lon, lat)
    :return: distance en kilomètres
    """
    url = f"{VALHALLA_URL}/route"
    locations = [{"lon": lon, "lat": lat} for lon, lat in coords]
    payload = {
        "locations": locations,
        "costing": "auto",
        "directions_options": {"units": "kilometers"}
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    # On prend la première route
    return data['trip']['summary']['length']


def match_passenger(
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
    # Trajet conducteur seul
    normal_distance = get_route_distance([driver_start, driver_end])
    # Trajet avec détour : A ➔ C ➔ D ➔ B
    detour_distance = get_route_distance([
        driver_start, passenger_start, passenger_end, driver_end
    ])
    extra_km = detour_distance - normal_distance
    print(f"Trajet normal: {normal_distance:.2f} km")
    print(f"Trajet avec détour: {detour_distance:.2f} km")
    print(f"Détour: {extra_km:.2f} km")
    return extra_km <= max_extra_km


if __name__ == "__main__":
    # Exemple test minimal autour d'Andorre (bbox ~1.4,42.4,1.6,42.6)
    print("--- Exemple 1 : Andorre-la-Vieille centre ---")
    driver_start = (1.521, 42.507)   # Andorre-la-Vieille centre
    driver_end = (1.528, 42.513)     # Quartier nord
    passenger_start = (1.523, 42.509) # Quartier est
    passenger_end = (1.524, 42.510)   # Quartier est
    is_match = match_passenger(driver_start, driver_end, passenger_start, passenger_end, max_extra_km=2.0)
    print("Match!" if is_match else "Pas de match.")

    print("\n--- Exemple 2 : détour raisonnable ---")
    driver_start = (1.521, 42.507)   # Andorre-la-Vieille centre
    driver_end = (1.528, 42.513)     # Quartier nord
    passenger_start = (1.45, 42.45) # Sud-Ouest (limite bbox)
    passenger_end = (1.45, 42.45)
    is_match = match_passenger(driver_start, driver_end, passenger_start, passenger_end, max_extra_km=3.0)
    print("Match Sud-Ouest!" if is_match else "Pas de match Sud-Ouest.")

    print("\n--- Exemple 3 : détour trop grand ---")
    passenger_start = (1.6, 42.6)   # Nord-Est (limite bbox)
    passenger_end = (1.6, 42.6)
    is_match = match_passenger(driver_start, driver_end, passenger_start, passenger_end, max_extra_km=1.0)
    if is_match:
        print("Match Nord-Est!")
    else:
        print(f"Désolé, le détour pour récupérer ce passager au Nord-Est dépasse 1 km. Pas de match.")
