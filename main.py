from flask import Flask, render_template
import pandas as pd

app = Flask("__name__")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def station(station, date):
    df = pd.read_csv(
        "data/data_stations/TG_STAID" + str(station).zfill(6) + ".txt",
        skiprows=20,
        parse_dates=["    DATE"],
    )
    temp = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    return {
        "station": station,
        "date": date,
        "temperature": temp,
    }


if __name__ == "__main__":
    app.run(debug=True, port=5000)
