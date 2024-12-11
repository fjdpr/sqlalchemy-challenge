# Import the dependencies
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################
# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Print all of the classes mapped to the Base
print(Base.classes.keys())

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available routes."""
    return (
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>" 
        f"Link for specific date consultation, example: 2010-01-01<br/><br/>" 
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>" 
        f"Link for specific date range, example: 2010-01-01/2017-08-23<br/><br/>"
        f"The database ranges are:<br/>"
        f"2010-01-01<br/>"
        f"2017-08-23<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months."""
    # Create a session
    session = Session(engine)
    
    # Calculate the date one year ago from the last date in the data set
    recent_date = session.query(func.max(Measurement.date)).scalar()
    recent_date_dt = dt.datetime.strptime(recent_date, '%Y-%m-%d')
    one_year_ago = recent_date_dt - dt.timedelta(days=366)

    # Perform a query to retrieve the data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    session.close()

    # Convert the query results to a dictionary
    precipitation_list = [{"date": date, "prcp": prcp} for date, prcp in precipitation_data]
    
    return jsonify(precipitation_list)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations."""
    # Create a session
    session = Session(engine)
    
    # Query to get all stations
    results = session.query(Station.station, Station.name).all()
    
    session.close()

    # Convert the list of tuples into a list
    stations_list = [{"station": station, "name": name} for station, name in results]

    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the previous year for the most active station."""
    # Create a session
    session = Session(engine)
    
    # Calculate the date one year ago from the last date in data set
    recent_date = session.query(func.max(Measurement.date)).scalar()
    recent_date_dt = dt.datetime.strptime(recent_date, '%Y-%m-%d')
    one_year_ago = recent_date_dt - dt.timedelta(days=366)

    # Find the most active station
    active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    # Query the temperature observations for the previous year
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == active_station).\
        filter(Measurement.date >= one_year_ago).all()
    
    session.close()

    # Convert the query results to a list of dictionaries
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in tobs_data]

    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    """Return the min, avg, and max temperatures for a given start or start-end range."""
    # Create a session
    session = Session(engine)
    
    if not end:
        # Calculate TMIN, TAVG, and TMAX for dates greater than or equal to the start date
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date == start).all()
    else:
        # Calculate TMIN, TAVG, and TMAX for dates from the start date to the end date (inclusive)
        results = session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs)
        ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    # Convert the query results to a list
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }

    return jsonify(temp_stats)


if __name__ == '__main__':
    app.run(debug=True)
