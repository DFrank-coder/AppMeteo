from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "75796f8b777efd7396c248b6cb51e696"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    clima = None
    error = None

    if request.method == "POST":
        ciudad = request.form.get("ciudad")
        respuesta = requests.get(BASE_URL, params={
            "q": ciudad,
            "appid": API_KEY,
            "units": "metric",
            "lang": "es"
        })

        if respuesta.status_code == 200:
            datos = respuesta.json()
            clima = {
                "ciudad": datos["name"],
                "pais": datos["sys"]["country"],
                "temperatura": round(datos["main"]["temp"]),
                "sensacion": round(datos["main"]["feels_like"]),
                "humedad": datos["main"]["humidity"],
                "viento": round(datos["wind"]["speed"] * 3.6),
                "descripcion": datos["weather"][0]["description"].capitalize(),
                "icono": datos["weather"][0]["icon"],
            }
        else:
            error = "Ciudad no encontrada. Verificá el nombre e intentá de nuevo."

    return render_template("index.html", clima=clima, error=error)

if __name__ == "__main__":
    app.run(debug=True)