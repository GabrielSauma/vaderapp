Väderappen

Beskrivning
En väderapp byggd med Python och Flask. Appen hämtar väderdata från Open-Meteo api och visar aktuellt väder samt en väderprognos för kommande tre dagar.

Användaren kan välja mellan dessa fem städer:
Stockholm
Göteborg
Malmö
Umeå
Kiruna

Installation

1. Klona projektet från GitHub:
git clone https://github.com/GabrielSauma/vaderapp.git

2. Skapa och aktivera en virtuell miljö:

Windows PowerShell:

py -m venv venv

macOS/Linux Bash:

python3 -m venv venv

3. Aktivera den virtuella miljön

Windows PowerShell:

.\venv\Scripts\Activate.ps1

Windows CMD:

venv\Scripts\activate.bat

macOS/Linux Bash:

source venv/bin/activate

4. Installera projektets requirements:
Kör följande kommando när den virtuella miljön är aktiverad(venv):
python -m pip install -r requirements-dev.txt

Köra applikationen

Starta väderappen med:
python app.py
Öppna sedan http://127.0.0.1:5000/ i webbläsaren.

Ruff – kodkontroll

Kontrollera koden med:
ruff check .

Formatera koden med:
ruff format .

Köra tester

Kör testerna med:
python -m pytest -v


Uppgiftens frågor
1. Varför mockar du anropen mot API:et i dina tester, och vad skulle hända om du inte gjorde 
det?

Svar:
Jag mockar anropen till api:et i testerna för att de ska fungera utan internet och utan att behöva riktig väderdata. Om man inte mockar anropen skulle testerna behöva en internetanslutning för att nå api:et, vilket kan göra testerna mindre tillförlitliga.

2. Vad gör timeout och raise_for_status(), och varför behövs de?

Svar:
timeout begränsar hur länge programmet väntar på svar från api:et och raise_for_status() kontrollerar om servern svarat med ett hhtp-fel.
timeout och raise_for_status() behövs för att programmet inte ska vänta för länge eller fortsätta arbeta med ett felaktigt api svar.

3. Hur fungerar mallarv i Jinja2? Förklara med exempel från dina egna mallar.

Svar:
Mallarv i Jinja2 fungerar genom att flera html filer kan använda en gemensam grundmall istället för att upprepa samma html kod i flera filer.
I väderappen använder index.html, om.html, vader.html och 404.html grundmallen base.html. Filerna använder {% extends "base.html" %} för att få den gemensamma navigeringen och fyller grundmallens block med eget innehåll.


4. Vad är en fixture, och vilken använder du?

Svar:
En fixture i Pytest är en funktion som förbereder data som kan användas av flera tester i testfilen. På så sätt behöver man inte upprepa samma kod i flera tester.
I test_app.py använder jag klient, som skapar en testklient för Flask, och api_svar som innehåller exempel på väderdata.