from flask import Flask, render_template
import pandas as pd

app = Flask("__name__")

stations_table = pd.read_csv(
    "data/data_stations/stations.txt",
    skiprows=17,
)


@app.route("/")
def home():
    return render_template("home.html", data=stations_table.to_html())


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


@app.route("/api/v1/<station>")
def all_station_info(station):
    df = pd.read_csv(
        "data/data_stations/TG_STAID" + str(station).zfill(6) + ".txt",
        skiprows=20,
        parse_dates=["    DATE"],
    )
    info = df.to_dict(orient="records")
    return info


@app.route("/api/v1/yearly/<station>/<year>")
def year_info(station, year):
    df = pd.read_csv(
        "data/data_stations/TG_STAID" + str(station).zfill(6) + ".txt",
        skiprows=20,
    )
    df["    DATE"] = df["    DATE"].astype(str)
    info = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    print(info)
    return info


if __name__ == "__main__":
    app.run(debug=True, port=5000)
