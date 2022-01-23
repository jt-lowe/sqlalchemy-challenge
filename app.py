import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

#setup Flask
app = Flask(__name__)

#setup the database
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect hawaii.sqlite database into a new model
Base = automap_base()

# reflect the tables contained in the file
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


#Define routes for activity


@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation - Returns a JSONified dictionary containing all dates between the most recent date in the dataset and a year prior, and their corresponding precipitation amount for that day (in inches) <br/><br/>"
        f"/api/v1.0/stations - Returns a JSONified list of stations in the dataset<br/><br/>"
        f"/api/v1.0/tobs - Returns a JSONified dictionary containing all dates between the most recent date in the dataset and a year prior, and their corresponding temperature observation data from the most active station<br/><br/>"        
        f"/api/v1.0/&ltstart> - Input a start date ::Format = YYYY-MM-DD (single M or D if single digit in date):: Returns a JSONified dictionary containing Average, Lowest and Highest temperature observation data for all dates between selected start date and the end of the dataset<br/><br/>"
        f"/api/v1.0/&ltstart>/&ltend> - - Input a start & end date ::Format = YYYY-MM-DD (single M or D if single digit in date):: Returns a JSONified dictionary containing Average, Lowest and Highest temperature observation data for all dates between selected start date and selected end date"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list containing the date and corresponding precipitation amount"""
    # Query precipitation data
    prcp_results = session.query(Measurement.date,Measurement.prcp).\
                filter(Measurement.date > dt.date(2016,8,23)).\
                order_by(Measurement.date).all()

    session.close()
    
    prcp_info = []
        
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_info.append(prcp_dict)
        
    return jsonify(prcp_info)


@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list containing each station in the dataset"""
    # Query precipitation data
    results = session.query(Station.station).all()

    session.close()
    
    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

        
    return jsonify(station_list)
    
    
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list containing the date and corresponding tobs value for our most active station"""
    
    #Find the most active station in the dataset
    most_active_station_query = session.query(Measurement.station).\
                                    group_by(Measurement.station).\
                                    order_by(func.count(Measurement.station).desc())
    most_active_station = session.execute(most_active_station_query).scalar()
    
    
    # Query temperatire observation data for most active station (we can use the same date for the year previous as we already found it in Step 1)
    tobs_results = session.query(Measurement.date,Measurement.tobs).\
                filter(Measurement.date > dt.date(2016,8,23)).\
                filter(Measurement.station == most_active_station).\
                order_by(Measurement.date).all()

    session.close()
    
    tobs_info = []
        
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_info.append(tobs_dict)
        
    return jsonify(tobs_info)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    start_results = session.query(func.min(Measurement.tobs)\
                                    ,func.avg(Measurement.tobs)\
                                    ,func.max(Measurement.tobs)).\
                                    filter(Measurement.date > start).\
                                    order_by(Measurement.date).all()
    
    session.close()
    
    start_info = []
        
    for TMIN,TAVG,TMAX in start_results:
        start_dict = {}
        start_dict["TMIN"] = TMIN
        start_dict["TAVG"] = TAVG
        start_dict["TMAX"] = TMAX
        start_info.append(start_dict)
        
    return jsonify(start_info)
    
    return start

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    
    session = Session(engine)
    
    start_end_results = session.query(func.min(Measurement.tobs)\
                                    ,func.avg(Measurement.tobs)\
                                    ,func.max(Measurement.tobs)).\
                                    filter(Measurement.date > start).\
                                    filter(Measurement.date <= end).\
                                    order_by(Measurement.date).all()
    
    session.close()
    
    start_end_info = []
        
    for TMIN,TAVG,TMAX in start_end_results:
        start_end_dict = {}
        start_end_dict["TMIN"] = TMIN
        start_end_dict["TAVG"] = TAVG
        start_end_dict["TMAX"] = TMAX
        start_end_info.append(start_end_dict)
        
    return jsonify(start_end_info)

if __name__ == "__main__":
    app.run(debug=True)
