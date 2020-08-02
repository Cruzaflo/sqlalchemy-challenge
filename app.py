#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


#home
@app.route("/")
def welcome():
    return(
        f"Hawaii Climate Analysis API <br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )


#Percipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prior_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prior_year).all()
    
    precip_dic = {date: prcp for date, prcp in precipitation}  
    return jsonify(precip_dic)

#Stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    prior_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs)
    results = results.filter(Measurement.station == "USC00519281", Measurement.date >= prior_year).all()
    
    tobs = list(np.ravel(results))
    return jsonify(tobs)

#Start and end
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),
func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).            filter(Measurement.date >= start).all()
        
        temps = list(np.ravel(results))
        return jsonify(temps)
        
    results = session.query(*sel).        filter(Measurement.date >= start).        filter(Measurement.date <= end).all()
    
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
    app.run()


# In[ ]:




