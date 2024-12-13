# Import the dependencies.
import numpy as np

import datetime as dt
from datetime import timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature for an entire year /api/v1.0/tobs<br/>"
        f"Temperature stat from start date (yyyy-mm-dd): /api/v1.0/<start>"
        f"Temperature stat from start to end dates (yyyy-mm-dd): /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    most_recent_date = session.query(func.max(Measurement.date).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    # Calculate the date one year from the last date in data set.
    first_date = most_recent_date - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    last_twelve_months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= first_date).all()
    # Convert to dictionary 
    precipitation_dictionary = {date: prcp for date, prcp in last_twelve_months}
    # Close the session
    session.close()
    # Jsonifify precipitation data over the last year
    return jsonify(precipitation_dictionary)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    # session = Session(engine)
    # Return a JSON list of stations from dataset.
    station_list = session.query(Station.station,Station.name).all()
    # Close
    session.closed()
    # Jsonify station data

@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date one year from the last date in data set.
    first_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    temperature_data = session.query(Measurement.tobs)\
    .filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date >= first_date)\
    .all()
    # Close
    session.closed()
    #Jsonify data for the previous 12 months
    return jsonify(tobs_list)

 @app.route("/api/v1.0/<start>)
    def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query of min, max and avg temperature for all dates greater or equal to the given date. 
    results = session.query(Measurement.date,func.min(Measurement.tobs,\
                                                      func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                                                        filter(Measurement.date >= start.all()
    # Close
    session.closed()

    # Jsonify min, avg, and max temps for specific start
    return jsonify (start_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date:
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query of min, max and avg temperature for all dates greater or equal to the given date. 
    results = session.query(func.min(Measurement.tobs,\
                                                      func.avg(Measurement.tobs), func.max(Measurement.tobs)),\
                                                        filter(Measurement.date >= start).filter(Measurement.date <= end.all()
    # Close
    session closed()
    #Jsonify min, avg, and max temps for specific start-end date range
    return jsonify(info)