# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station


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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return precipitation"""
    results = session.query(Measurement.date, Measurement.prcp )\
        .filter(Measurement.date >= '2016-08-23')\
        .filter(Measurement.prcp.isnot(None)) \
        .all()
    
    session.close()

    resutls_list = list(np.ravel(results))

    result_dict = {}


    for i in range(0, len(resutls_list), 2):
        date = resutls_list[i]
    
        if i + 1 < len(resutls_list):
            number = resutls_list[i + 1]
            result_dict[date] = number
        else:
            result_dict[date] = None

    return jsonify(result_dict)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.name).all()

    session.close()

    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query( Measurement.tobs )\
                    .filter(Measurement.date >= '2016-08-23')\
                    .filter(Measurement.station == "USC00519281")\
                    .all()

    session.close()

    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs) )\
            .filter(Measurement.date > start)\
            .all()

    session.close()

    results_list = list(np.ravel(results))

    final_result = {"Min": results_list[0], "Max": results_list[1], "Avg": results_list[2]}


    return jsonify(final_result)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs) )\
            .filter(Measurement.date > start)\
            .filter(Measurement.date < end)\
            .all()

    session.close()

    results_list = list(np.ravel(results))

    final_result = {"Min": results_list[0], "Max": results_list[1], "Avg": results_list[2]}

    return jsonify(final_result)



if __name__ == '__main__':
    app.run(debug=True)



