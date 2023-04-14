import sqlalchemy as _sql
from app.db.database_connection import Base


class WeatherRecordDB(Base):
    __tablename__ = "weather_data_record"
    id = _sql.Column(_sql.Integer, primary_key=True, autoincrement=True)
    station_id = _sql.Column(_sql.String(20))
    date = _sql.Column(_sql.String(25))
    max_temperature = _sql.Column(_sql.Float)
    min_temperature = _sql.Column(_sql.Float)
    precipitation = _sql.Column(_sql.Float)


class WeatherStatsDB(Base):
    __tablename__ = "weather_stats"
    id = _sql.Column(_sql.Integer, primary_key=True)
    station_id = _sql.Column(_sql.String(20))
    year = _sql.Column(_sql.String(4))
    avg_max_temperature = _sql.Column(_sql.Float)
    avg_min_temperature = _sql.Column(_sql.Float)
    total_precipitation = _sql.Column(_sql.Float)
