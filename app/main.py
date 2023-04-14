import fastapi
import uvicorn as uvicorn

from fastapi_pagination import add_pagination

from app import health
from app.service.weather_data_service import WeatherService
from app.db import database_connection
from app.routes import weather_routes

database_connection.create_database()

api = fastapi.FastAPI()


# Configure the application by adding routers
def configure():
    api.include_router(health.router)
    api.include_router(weather_routes.router)


configure()

# Add pagination to the FastAPI application
add_pagination(api)

if __name__ == '__main__':

    # Ingest test data into the application and perform data analysis
    WeatherService().ingest_data('../data/test_data')
    WeatherService().weather_data_analysis()

    uvicorn.run("main:api", port=8000)
