#!/usr/bin/env python
# coding: utf-8

# In[9]:


import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# In[10]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
#################################################
app = Flask(__name__)
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List of dates and percipitation observations from the last year<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of stations from the dataset<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of Temperature Observations (tobs) for the previous year<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- List of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- List of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range, inclusive<br/>"

    )

@app.route("/api/v1.0/precipitation")

def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the JSON representation of your dictionary."""
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    dates = {}
    for result in results:
        dates[result[0]]=result[1]

    return jsonify(dates)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    # Query the dates and temperature observations of the most active station for the last year of data.
    one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.date >= one_year_date).filter(Measurement.station == 'USC00519281').all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/<start>")
def startdates(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start = dt.date(2017, 2, 10)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >=start).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/<start>/<end>")
def startenddates(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start = dt.date(2017, 2, 10)
    end = dt.date(2017, 2, 25)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >=start).filter(Measurement.date <=end).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




