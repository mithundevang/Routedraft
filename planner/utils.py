import requests
import math
from django.conf import settings


# ================= GET COORDINATES =================
def get_coordinates(destination):
    url = "https://api.opentripmap.com/0.1/en/places/geoname"

    params = {
        "name": destination,
        "apikey": settings.OPENTRIPMAP_API_KEY
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        return None, None

    data = response.json()
    return data.get("lat"), data.get("lon")


# ================= GET ATTRACTIONS =================
def get_attractions(lat, lon):

    kinds_list = [
        "interesting_places",
        "museums",
        "castles",
        "palaces",
        "viewpoints",
        "gardens_and_parks"
    ]

    attractions = []

    for kind in kinds_list:

        url = "https://api.opentripmap.com/0.1/en/places/radius"

        params = {
            "radius": 50000,
            "lon": lon,
            "lat": lat,
            "kinds": kind,
            "limit": 20,
            "format": "json",
            "apikey": settings.OPENTRIPMAP_API_KEY
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            continue

        data = response.json()

        for place in data:

            name = place.get("name")
            point = place.get("point")

            if not name or not point:
                continue

            attractions.append({
                "name": name,
                "lat": point.get("lat"),
                "lon": point.get("lon"),
                
            })

    return attractions


# ================= DISTRIBUTE DAYS =================
def distribute_days(attractions, days):
    if not attractions:
        return {i + 1: [] for i in range(days)}

    itinerary = {}
    per_day = math.ceil(len(attractions) / days)

    for i in range(days):
        itinerary[i + 1] = attractions[i * per_day:(i + 1) * per_day]

    return itinerary