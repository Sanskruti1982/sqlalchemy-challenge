# 1. Import Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        "<br/>"
        f"Information about precipitation from Aug 2016 to Aug 2017:/api/v1.0/precipitation<br/>"
        "<br/>"
        f"Information about stations: /api/v1.0/stations<br/>"
        "<br/>"
        f"Information about temperature from Aug 2016 to Aug 2017:/api/v1.0/tobs<br/>"
        "<br/>"
        f"Information on min, max and avg temperature for start date provided (format:yyyy-mm-dd):/api/v1.0/<start><br/>"
        "<br/>"
        f"Information on min, max and avg temperature for start and end date provided (start date format:yyyy-mm-dd/end date format:yyyy-mm-dd):/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all date and prcp
    query_dt = session.query(Measurement.date).order_by(Measurement.date.desc()).group_by(Measurement.date).limit(1).all()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_date_prcp
    all_date_prcp = []
    for date, prcp in results:
        dateprcpdict = {}
        dateprcpdict["Date"] = date
        dateprcpdict["Prcp"] = prcp
        all_date_prcp.append(dateprcpdict)

    return jsonify(all_date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all station
    results = session.query(Station.station).all()

    session.close()

     # Convert list of tuples into normal list
    all_stations = []
    for station in results:
        stats = {}
        stats["Station"] = station
        all_stations.append(stats)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all tobs for all of previous year
    query_dt = session.query(Measurement.date).order_by(Measurement.date.desc()).group_by(Measurement.date).limit(1).all()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= query_date).all()

    session.close()

     # Convert list of tuples into normal list
    all_tobs = []
    for date, tobs in results:
        alltobs = {}
        alltobs["Date"] = date
        alltobs["tobs"] = tobs
        all_tobs.append(alltobs)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all min, max and avg tobs for start date specified 
    sel = [(Measurement.date),func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start).all()

    session.close()

     # Convert list of tuples into normal list
    all_sd = []
    for date, mint, avgt, maxt in results:
        allsds = {}
        allsds["Date"] = date
        allsds["Min Temp"] = mint
        allsds["Avg Temp"] = avgt
        allsds["Max Temp"] = maxt
        all_sd.append(allsds)

    return jsonify(all_sd)

@app.route("/api/v1.0/<start>/<end>")
def Startend(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

     # Query all min, max and avg tobs for start date and end date specified 
    sel = [(Measurement.date),func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

     # Convert list of tuples into normal list
    all_sded = []
    for date, mint, avgt, maxt in results:
        allsded = {}
        allsded["Date"] = date
        allsded["Min Temp"] = mint
        allsded["Avg Temp"] = avgt
        allsded["Max Temp"] = maxt
        all_sded.append(allsded)
    return jsonify(all_sded)

if __name__ == '__main__':
    app.run(debug=True)