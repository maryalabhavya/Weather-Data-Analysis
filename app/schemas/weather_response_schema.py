from pydantic import BaseModel


# Define two Pydantic models to represent the data returned by the API.
class WeatherRecordItem(BaseModel):
    station_id: str
    date: str
    min_temperature: float
    max_temperature: float
    precipitation: float


class WeatherStatsItem(BaseModel):
    station_id: str
    year: str
    avg_min_temperature: float
    avg_max_temperature: float
    total_precipitation: float
