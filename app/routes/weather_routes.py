import fastapi
import sqlalchemy.orm as _orm
from fastapi import Query
from fastapi_pagination import Page, paginate

import app.db.database_connection as _db_connection
from app.service.weather_data_service import WeatherService
from app.schemas.weather_response_schema import WeatherRecordItem, WeatherStatsItem

router = fastapi.APIRouter()


@router.get('/api/weather', summary='Get Weather Records', response_model=Page[WeatherRecordItem])
def get_weather_data(station_id: str = Query(..., example='USC00110072'), date: str = Query(..., example='1985-01-01'),
                     db: _orm.Session = fastapi.Depends(_db_connection.get_db)):
    # TODO: Add Pagination Logic
    return paginate(WeatherService(db=db).get_weather_record(station_id=station_id, date=date))


@router.get('/api/weather/stats', summary='Get Weather Stats', response_model=Page[WeatherStatsItem])
def get_weather_stats(station_id: str = Query(..., example='USC00110072'), date: str = Query(..., example='1985-01-01'),
                      db: _orm.Session = fastapi.Depends(_db_connection.get_db)):
    return paginate(WeatherService(db=db).get_weather_stats(station_id=station_id, year=date[:4]))
