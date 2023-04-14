import fastapi
import sqlalchemy.orm as _orm
import app.db.database_connection as _db_connection
from app.service.weather_data_service import WeatherService

router = fastapi.APIRouter()


@router.get('/api/weather', summary='Get Weather Records')
def get_weather_data(station_id: str, date: str,
                     db: _orm.Session = fastapi.Depends(_db_connection.get_db)):
    # TODO: Add Pagination Logic
    return WeatherService(db=db).get_weather_record(station_id=station_id, date=date)


@router.get('/api/weather/stats', summary='Get Weather Stats')
def get_weather_stats(station_id: str, date: str,
                      db: _orm.Session = fastapi.Depends(_db_connection.get_db)):
    return WeatherService(db=db).get_weather_stats(station_id=station_id, year=date[:4])
