import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)


@app.route("/")
def home():
    return (
          f"Available Routes:<br/>"
         f"/api/v1.0/precipitation"
         f"- Dates and temperature observations from the last year<br/>"

         f"/api/v1.0/stations"
         f"- List of stations<br/>"

         f"/api/v1.0/tobs"
         f"- Temperature Observations from the past year<br/>"

         f"/api/v1.0/<start>"
         f"- Minimum temperature, the average temperature, and the max temperature for a given start day<br/>"

         f"/api/v1.0/<start>/<end>"
         f"- Minimum temperature, the average temperature, and the max temperature for a given start-end range<br/>"
     )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Query
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_date = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    last_date = session.query(Station.name).group_by(Station.name).all()

    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').filter(Measurement.date < '2017-08-23').order_by(Measurement.date).all()
    temp_last_year=[]
    for date, temperature in results:
        temp_dict={}
        temp_dict["date"] = date
        temp_dict["tobs"] = temperature
        temp_last_year.append(temp_dict)

    return jsonify(temp_data)

@app.route("/api/v1.0/<start>")
def start(start):
 
    session = Session(engine)

    summary=[]
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date > start).all()
                                
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date > start).all()
                                
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > start).all()
                           
    summary.append(min_temp)
    summary.append(max_temp)
    summary.append(avg_temp)

    return jsonify(summary)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)
    summary=[]
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).all()                    
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).all()                         
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).all()            
    
    summary.append(min_temp)
    summary.append(max_temp)
    summary.append(avg_temp)

    return jsonify(summary)
    
if __name__ == '__main__':
    app.run(debug=True)