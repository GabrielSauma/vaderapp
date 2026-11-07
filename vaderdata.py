import requests

# Lista med de fem giltiga städerna
städer = ["Stockholm", "Göteborg", "Malmö", "Umeå", "Kiruna"]

def är_giltig_stad(stad):
    """Kontrollerar om staden finns i bland de giltiga städerna."""
    return stad in städer

# Koordinater för de fem städerna
koordinater = {
    "Stockholm": (59.33, 18.07),
    "Göteborg": (57.71, 11.97),
    "Malmö": (55.61, 13.00),
    "Umeå": (63.83, 20.26),
    "Kiruna": (67.86, 20.23),
}

def hämta_koordinater(stad):
    """Hämtar koordinaterna för en stad."""
    return koordinater.get(stad)


def hämta_väderdata(stad):
    """Hämtar väderdata från Open-Meteo."""

    koordinat = hämta_koordinater(stad)

    if koordinat is None:
        return None

    latitud, longitud = koordinat

    url = "https://api.open-meteo.com/v1/forecast"

    parametrar = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 3,
    }

    try:
        # Skickar en förfrågan till Open-Meteo
        svar = requests.get(url, params=parametrar, timeout=10)
        svar.raise_for_status()

        return svar.json()

    except requests.RequestException as e:
        raise Exception("Kunde inte hämta väderdata.") from e