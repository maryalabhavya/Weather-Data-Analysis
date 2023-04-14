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
    """
    Endpoint to get weather records for a given station and date.

    :param station_id: str, required, station id for which the weather records are requested.
    :param date: str, required, date for which the weather records are requested in yyyy-mm-dd format.
    :param db: _orm.Session, required, database session object.

    :return: Page[WeatherRecordItem], a paginated list of WeatherRecordItem objects.
    """
    return paginate(WeatherService(db=db).get_weather_record(station_id=station_id, date=date))


@router.get('/api/weather/stats', summary='Get Weather Stats', response_model=Page[WeatherStatsItem])
def get_weather_stats(station_id: str = Query(..., example='USC00110072'), date: str = Query(..., example='1985-01-01'),
                      db: _orm.Session = fastapi.Depends(_db_connection.get_db)):
    """
    Endpoint to get weather stats for a given station and year.

    :param station_id: str, required, station id for which the weather stats are requested.
    :param date: str, required, year for which the weather stats are requested in yyyy format.
    :param db: _orm.Session, required, database session object.

    :return: Page[WeatherStatsItem], a paginated list of WeatherStatsItem objects.
    """
    return paginate(WeatherService(db=db).get_weather_stats(station_id=station_id, year=date[:4]))
