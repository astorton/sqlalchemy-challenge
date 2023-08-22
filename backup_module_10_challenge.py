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
        "Welcome to the Climate App!"\
        f"/api/v1.0/precipitation"\
        f"/api/v1.0/stations"\
        f"/api/v1.0/tobs"
        f"/api/v1.0/please enter a date"
        f"/api/v1.0/please enter a start and end date"
    )

    station_list = session.query(station).all()

#################################################
# Flask Routes
@app.route("/api//v1.0/precipitation")
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
    
@app.route("/api//v1.0/stations")
def stations():
    session = Session(hw_engine)

    #Return a complete list of all stations with the date as the key; looking back one year back"""
    station_list = session.query(station.station).all()
    station_count = session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()
    session.close()

    all_stations = list(np.ravel(station_list))
    all_counts =list(np.ravel (station_count))

    return jsonify(all_stations,station_count)

@app.route("/api/v1.0/tobs")
def tobs():
    #Return the most active station and the last year of temp. data
    session = Session(hw_engine)

    #return the latest date for the 
    mas_one_year_lookback = dt.date(2017,8,18) - timedelta(days=365)
    mas_tobs_data = session.query(measurement.tobs).filter(measurement.date >= mas_one_year_lookback).all()

    session.close()

    all_temps = list(np.ravel(mas_tobs_data))

    return jsonify(all_temps)


# Return list of the min. temp., avg. temp. and max. temp. for a specific time period. 
#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>")

def start_date(start):
    """Fetch the start date that matches the path variable supplied by the user, or prompt a 404 error if not."""
    session = Session(hw_engine)
    if start == None:
    
        return jsonify({"error": f"Character with real_name {start} not found."}), 404

    else:
        start_query = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.date >= start).group_by(measurement.date).all()
        session.close()
    
    start_date_results = []

    session.close()

    start_date_dict = {}
    start_date_dict["Min Temp"] = start_query[0][0]
    start_date_dict["Max Temp"] = start_query[0][1]
    start_date_dict["Avg Temp"] = start_query[0][2] 
    return jsonify(start_date_dict)

@app.route("/api/v1.0/<start>/<end>")

def alpha_omega(start, end):
    # Create our session (link) from Python to the DB
  
    
    #return the queried data bounded between the start and end dates
    sel = [func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)]
    start=dt.datetime.strptime(start, "%m%d%Y")
    results =session.query(*sel).filter(measurement.date >= start).filter(measurement.date <= end)
    session.close()
    temps = list(np.ravel(results))

    
    return jsonify(temps)

# for date, min, max, avg in alpha_omega:
#     start_date_dict = {}
#     start_date_dict["Date"] = a_o_results[0][0]
#     start_date_dict["TMIN"] = min 
#     start_date_dict["TMAX"] = max
#     start_date_dict["TAVG"] = avg 
#     a_o_list.append(start_date_dict)

if __name__ == "__main__":
    app.run(debug=True)

#################################################
