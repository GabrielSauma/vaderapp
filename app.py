from flask import Flask, render_template, request

import vaderdata

app = Flask(__name__)

städer = ["Stockholm", "Göteborg", "Malmö", "Umeå", "Kiruna"]


@app.route("/")
def startsida():
    stad = request.args.get("stad")

    if stad is None:
        return render_template("index.html")

    if stad not in städer:
        return "Ogiltig stad"

    try:
        väderdata = vaderdata.hämta_väderdata(stad)

    except vaderdata.VäderdataFel:
        return "Kunde inte hämta väderdata"

    if väderdata is None:
        return "Kunde inte hitta staden"

    prognos = vaderdata.omvandla_väderdata(väderdata)

    return render_template(
        "index.html", stad=stad, aktuell_väder=väderdata["current"], prognos=prognos
    )


if __name__ == "__main__":
    app.run(debug=True)
