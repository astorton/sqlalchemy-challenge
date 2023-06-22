# Import the dependencies.
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import timedelta



#################################################
# Database Setup
#################################################
hw_engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
base = automap_base()


# reflect the tables
base.prepare(hw_engine, reflect=True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(hw_engine)

row_one = session.query(measurement).first()
row_one.__dict__

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
    #List available api routes.
    return (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
    )

    station_list = session.query(station).all()

#################################################
# Flask Routes
@app.route("/api/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(hw_engine)

    #Return a list of all percipitation data with the date as the key; looking back one year back"""
    one_year_lookback = dt.date(2017,8,23) - timedelta(days=365)
    measurement_tp = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_lookback).all()
    measurement_tp
    
    session.close()

    # Convert list of tuples into normal list
    all_measurements = list(np.ravel(measurement_tp))

    return jsonify(all_measurements)
    
@app.route("/api/stations")
def stations():
    session = Session(hw_engine)

    #Return a complete list of all stations with the date as the key; looking back one year back"""
    station_list = session.query(station.station).all()

    session.close()

    all_stations = list(np.ravel(station_list))

    return jsonify(all_stations)

@app.route("/api/tobs")
def stations():
    #Return the most active station and the last year of temp. data
    stations_count = session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()
    mas_latest_date = session.query(func.max(measurement.date)).filter(measurement.station =='USC00519281').all()
    mas_one_year_lookback = dt.date(2017,8,18) - timedelta(days=365)
    mas_tobs_data = session.query(measurement.tobs).filter(measurement.date >= mas_one_year_lookback).all()

    session.close()

    all_temps = list(np.ravel(mas_tobs_data))

    return jsonify(all_temps)


# Return list of the min. temp., avg. temp. and max. temp. for a specific time period. 
#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/<start>")
def start_date(start):
    """Fetch the start date that matches the path variable supplied by the user, or prompt a 404 error if not."""
    for user_date in measurement.date:
        if user_date == measurement.date:
            return jsonify(user_date)

    return jsonify({"error": f"Character with real_name {start} not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)

#################################################
