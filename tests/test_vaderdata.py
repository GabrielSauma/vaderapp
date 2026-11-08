from unittest.mock import patch

import pytest
import requests

import vaderdata
from app import app
from vaderdata import hämta_väderdata, är_giltig_stad


@pytest.fixture
def klient():
    """Skapar en testklient för Flask-applikationen."""

    app.config.update(TESTING=True)

    return app.test_client()


@pytest.mark.parametrize("stad", ["Stockholm", "Göteborg", "Malmö", "Umeå", "Kiruna"])
def test_giltiga_städer(stad):
    assert är_giltig_stad(stad) is True


@pytest.mark.parametrize(
    "stad",
    ["London", "Oslo", "Paris", ""],
)
def test_ogiltiga_städer(stad):
    assert är_giltig_stad(stad) is False


def test_hämta_väderdata():
    """Testar att väderdata hämtas korrekt från API."""

    api_svar = {
        "current": {
            "temperature_2m": 12.5,
            "wind_speed_10m": 8.2,
        },
        "daily": {
            "time": ["2026-11-07", "2026-11-08", "2026-11-09"],
            "temperature_2m_max": [14, 13, 12],
            "temperature_2m_min": [7, 6, 5],
            "precipitation_sum": [0, 2, 1],
        },
    }

    with patch("vaderdata.requests.get") as simulerad_anrop:
        simulerad_anrop.return_value.json.return_value = api_svar

        resultat = hämta_väderdata("Stockholm")

        assert resultat == api_svar


def test_omvandla_väderdata():
    """Testar att väderdata omvandlas till en lista."""

    api_svar = {
        "daily": {
            "time": ["2026-11-07", "2026-11-08", "2026-11-09"],
            "temperature_2m_max": [14, 13, 12],
            "temperature_2m_min": [7, 6, 5],
            "precipitation_sum": [0, 2, 1],
        }
    }

    resultat = vaderdata.omvandla_väderdata(api_svar)

    förväntat_resultat = [
        {"datum": "2026-11-07", "max_temp": 14, "min_temp": 7, "nederbord": 0},
        {"datum": "2026-11-08", "max_temp": 13, "min_temp": 6, "nederbord": 2},
        {"datum": "2026-11-09", "max_temp": 12, "min_temp": 5, "nederbord": 1},
    ]

    assert resultat == förväntat_resultat


def test_hämta_väderdata_timeout():
    """Testar att timeout hanteras."""

    with patch("vaderdata.requests.get") as simulerat_anrop:
        simulerat_anrop.side_effect = requests.Timeout

        with pytest.raises(vaderdata.VäderdataFel):
            hämta_väderdata("Stockholm")


def test_hämta_väderdata_http_fel():
    """Testar att HTTP-fel hanteras."""

    with patch("vaderdata.requests.get") as simulerat_anrop:
        simulerat_anrop.return_value.raise_for_status.side_effect = requests.HTTPError

        with pytest.raises(vaderdata.VäderdataFel):
            hämta_väderdata("Stockholm")


def test_404_sida(klient):
    """Testar att en egen felsida visas vid ökänd adress."""

    svar = klient.get("/sidan_finns_inte")

    assert svar.status_code == 404
    assert b"Sidan kunde inte hittas" in svar.data
