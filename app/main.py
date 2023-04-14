import fastapi
import uvicorn as uvicorn
import logging

from app import health
from app.service.weather_data_service import WeatherService
from app.db import database_connection

logger = logging.getLogger()
logger.setLevel(logging.INFO)

database_connection.create_database()

WeatherService().ingest_data('../data/test_data')


api = fastapi.FastAPI()


def configure():
    api.include_router(health.router)


configure()


if __name__ == '__main__':
    uvicorn.run("main:api", port=8000)
