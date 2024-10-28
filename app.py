#!/usr/bin/python3

import arrow
import requests
import geocoder
from flask import Flask, render_template


OPEN_WEATHER_MAP_API_KEY = "95c24917f8cc445dad4ea6113a933807"
STORMGLASS_API_KEY = (
    "450880fc-7997-11eb-8302-0242ac130002-4508816a-7997-11eb-8302-0242ac130002"
)



app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/data")
def get_data():
    return {
        "openweathermap": get_open_weather_map_data(),
        "stormglass": get_stormglass_data(),
    }


def get_open_weather_map_data():
    x, y = geocoder.ip("me").latlng
    dt = int(arrow.now().floor('day').timestamp())

    exclude = "current,alerts,minutely"
    api_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+str(x)+"&lon="+str(y)+"&exclude="+exclude+"&appid="+{OPEN_WEATHER_MAP_API_KEY}+"&units=metric"

    response = requests.get(api_url)
    return response.json()


def get_stormglass_data():
    x, y = geocoder.ip("me").latlng

    # Get first hour of today
    start = arrow.now().floor('day')

    # Get last hour of today
    end = arrow.now().ceil("day")

    response = requests.get(
        "https://api.stormglass.io/v2/weather/point",
        params={
            "lat": x,
            "lng": y,
            "params": ",".join(["waveHeight", "airTemperature"]),
            "start": start.to("UTC").timestamp(),  # Convert to UTC timestamp
            "end": end.to("UTC").timestamp(),  # Convert to UTC timestamp
        },
        headers={"Authorization": STORMGLASS_API_KEY},
    )
    return response.json()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
