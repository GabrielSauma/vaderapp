from flask import Flask, render_template, request

import vaderdata

# Skapar flask applikationen
app = Flask(__name__)


# Skapar en egen Jinja2 filter som beskriver temperaturen
@app.template_filter("temperatur_text")
def temperatur_text(temperatur):
    """Beskriver temperaturen med en enkel text."""

    if temperatur < 0:
        return "Minusgrader"
    elif temperatur < 10:
        return "Kallt"
    elif temperatur < 20:
        return "Milt"
    else:
        return "Varmt"


# Visar startsidan där användaren kan välja stad
@app.route("/")
def startsida():
    """Visar startsidan där användaren kan välja stad."""
    return render_template("index.html")


# Hämtar och visar väderdata för vald stad
@app.route("/väder")
def vädersida():
    """Hämtar och visar väderdata för vald stad."""

    # Hämtar vald stad från URL
    stad = request.args.get("stad")

    # Kontrollerar om en giltig stad har valts
    if not vaderdata.är_giltig_stad(stad):
        return "Ogiltig stad", 400

    try:
        # Hämtar väderdata från api
        väderdata_resultat = vaderdata.hämta_väderdata(stad)

    except vaderdata.VäderdataFel:
        return "Kunde inte hämta väderdata", 503

    if väderdata_resultat is None:
        return "Kunde inte hitta staden", 404

    # Omvandlar api data till en väderprognos
    prognos = vaderdata.omvandla_väderdata(väderdata_resultat)

    # Visar väderet för den valda staden
    return render_template(
        "vader.html",
        stad=stad,
        aktuell_väder=väderdata_resultat["current"],
        prognos=prognos,
    )


# Visar information om väderappen
@app.route("/om")
def om_sida():
    """Visar information om väderappen."""
    return render_template("om.html")


# Hanterar sidor som inte finns
@app.errorhandler(404)
def sidan_hittades_inte(e):
    """Visar en egen felsida när en adress inte finns."""
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
