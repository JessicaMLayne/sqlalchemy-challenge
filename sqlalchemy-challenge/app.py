%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

inspector = inspect(engine)
inspector.get_table_names()

base = automap_base()
base.prepare(engine, reflect=True)


Station = base.classes.station
Measurement = base.classes.measurement

base.classes.keys()

mysession = Session(engine)

engine.execute('select max(measurement.date) from measurement').fetchall()

import datetime as dt

max_date=mysession.query(func.max(Measurement.date)).first()[0]

max_date_dt=dt.datetime.strptime(max_date, '%Y-%m-%d')
start_date_dt=max_date_dt-dt.timedelta(days=365)
start_date_dt

result=mysession.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=start_date_dt).all()

pd.DataFrame(result)

pd.DataFrame(result).plot(title="Precipitation")
plt.show()

pd.DataFrame(result).describe()

stations = mysession.query(Measurement.station).distinct().count()
print(f"Stations Available: {stations} ")

stations = mysession.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
print(f"Most Active Stations")
stations

most_active_station=stations[0][0]
print(f"Most Active Station: {most_active_station}")

most_active_temps = mysession.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.station == most_active_station).all()
print(f"Low: {most_active_temps[0][0]}")

most_active_temps = mysession.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.station == most_active_station).all()
print(f"High: {most_active_temps[0][1]}")

most_active_temps = mysession.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.station == most_active_station).all()
print(f"Average: {most_active_temps[0][2]}")

most_active_station=stations[0][0]
print(f"Most Active Station: {most_active_station}")

temperature_observations = mysession.query(Measurement.tobs).filter(Measurement.date >= start_date_dt).filter(Measurement.station == most_active_station).all()
temperature_observations = pd.DataFrame(temperature_observations, columns=['temperature'])

temperature_observations.plot.hist(bins=12, title="Temperature vs. Frequency")
plt.tight_layout()
plt.show()

