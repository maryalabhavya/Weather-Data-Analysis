import fastapi
import uvicorn as uvicorn
import logging

from app.service.weather_data_service import WeatherService
from app.db import database_connection
from app.routes import weather_routes

logger = logging.getLogger()
logger.setLevel(logging.INFO)

database_connection.create_database()

WeatherService().ingest_data('../data/test_data')
WeatherService().weather_data_analysis()


api = fastapi.FastAPI()


def configure():
    api.include_router(weather_routes.router)


configure()


if __name__ == '__main__':
    uvicorn.run("main:api", port=8000)
