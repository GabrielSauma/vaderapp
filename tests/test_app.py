from unittest.mock import patch

import pytest

from app import app


@pytest.fixture
def klient():
    """Skapar en testklient för Flask applikationen."""
    app.config.update(TESTING=True)
    return app.test_client()


@pytest.fixture
def api_svar():
    """Skapar exempel på väderdata från API."""
    return {
        "current": {
            "temperature_2m": 12.5,
            "wind_speed_10m": 8.2,
        },
        "daily": {
            "time": ["2026-11-08", "2026-11-09", "2026-11-10"],
            "temperature_2m_max": [14, 13, 12],
            "temperature_2m_min": [7, 6, 5],
            "precipitation_sum": [0, 2, 1],
        },
    }


def test_404_sida(klient):
    """Testar att en egen felsida visas vid en okänd adress."""
    svar = klient.get("/sidan_finns_inte")

    assert svar.status_code == 404
    assert b"Sidan kunde inte hittas" in svar.data


def test_startsida(klient):
    """Testar att startsidan visas korrekt."""
    svar = klient.get("/")

    assert svar.status_code == 200
    assert "Väderappen" in svar.get_data(as_text=True)


def test_vädersida(klient, api_svar):
    """Testar att vädersidan visar väderinformation."""

    # Simulerar svaret från väder API
    with patch("vaderdata.hämta_väderdata", return_value=api_svar):
        svar = klient.get("/väder?stad=Stockholm")

    assert svar.status_code == 200
    assert "Vädret i Stockholm" in svar.get_data(as_text=True)


def test_gemensam_navigering(klient, api_svar):
    """Testar att alla sidor har samma navigeringsmeny."""

    # Hämtar sidorna som ska testas
    svar = [
        klient.get("/"),
        klient.get("/om"),
        klient.get("/sidan_finns_inte"),
    ]

    # Simulerar väderdata för vädersidan
    with patch("vaderdata.hämta_väderdata", return_value=api_svar):
        svar.append(klient.get("/väder?stad=Stockholm"))

    # Kontrollerar att alla sidor har samma navigeringslänkar
    for sida in svar:
        innehåll = sida.get_data(as_text=True)

        assert 'href="/"' in innehåll
        assert 'href="/om"' in innehåll
