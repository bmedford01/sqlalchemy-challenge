### Do imports ###
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

### Set up Database connection ###
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)

# define classes
measurements = base.classes.measurement
stations = base.classes.station

### Set up Flask ###
app = Flask(__name__)

### Flask Routes ###
@app.route("/")
def home():
    return(
     f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperatures: /api/v1.0/tobs<br/>"
        f"Start Date: /api/v1.0/start<br/>"
        f"Start and End Dates: /api/v1.0/start_end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)
     #Query prcp data.
    results = session.query(measurements.date, measurements.prcp).\
    filter(measurements.date <= '2017-08-23').\
    filter(measurements.date >= '2016-08-23').\
    order_by(measurements.date.desc()).all()

    session.close()
   
    #Create dictionary from the query
    precipitation = []

    for date, prcp in results:
        precipt= {}
        precipt["date"] = date
        precipt["prcp"] = prcp
        precipitation.append(precipt)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    station_results = session.query(stations.station, stations.name).all()

    session.close()

    #create dictionary from the query
    stations = []

    for station, name in station_results:
        stns= {}
        stns["station"] = station
        stns["name"] = name
        stations.append(stns)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    temps = session.query(measurements.date).order_by(measurements.date.desc()).first()[0]
    dates = dt.datetime.strptime(temps, '%Y-%m-%d')
    date_query= dt.date(dates.year -1, dates.month, dates.day)
    search = session.query(measurements.tobs, measurements.date).filter(measurements.date >= date_query).all()

    session.close()

    #create dictionary from the query
    temperatures = []

    for tobs, date in search:
        temp= {}
        temp["date"] = date
        temp["tobs"] = tobs
        temperatures.append(temp)

    return jsonify(temperatures)

@app.route("/api/v1.0/start_date")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start_results = session.query(func.avg(measurements.tobs), func.max(measurements.tobs), func.min(measurements.tobs)).\
    filter(measurements.date >= start).all()

    session.close()

    #create dictionary from the query
    start_date = []

    for min, avg, max in start_results:
        start= {}
        start["avg"] = avg
        start["min"] = min
        start["max"] = max
        start_date.append(start)

    return jsonify(start_date)

@app.route("/api/v1.0/start_end")
def start_end(start, stop):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start_end_results = session.query(func.avg(measurements.tobs), func.max(measurements.tobs), func.min(measurements.tobs)).\
    filter(measurements.date >= start).filter(measurements.date <= stop).all()

    session.close()

    #create dictionary from the query
    start_end_dates = []

    for date, min, avg, max in start_end_results:
        start_end= {}
        start_end["avg"] = avg
        start_end["min"] = min
        start_end["max"] = max
        start_end_dates.append(start_end)

    return jsonify(start_end_dates)


if __name__ == "__main__":
    app.run(debug=True)
