import os
from datetime import datetime
import logging

from sqlalchemy import func

from app.models.weather_data_model import WeatherRecordDB, WeatherStatsDB
from app.db.database_connection import session
from app.schemas.weather_response_schema import WeatherRecordItem, WeatherStatsItem

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class WeatherService:
    # Initialize the WeatherService with the database session
    def __init__(self, db=session):
        self.db = db

    def ingest_data(self, data_path):
        # Ingest data from a directory of files
        ingestion_start_time = datetime.now()
        logging.info(f'Data Ingestion Start Time: {ingestion_start_time}')
        file_count = 0

        for filename in os.listdir(data_path):
            if filename.endswith('.txt'):
                file_count += 1
                file_path = os.path.join(data_path, filename)
                station_id = filename.split('.')[0]
                self.ingest_data_from_file(file_path=file_path, station_id=station_id)

        ingestion_end_time = datetime.now()
        logging.info(f'Data Ingestion End Time: {ingestion_end_time}')
        logging.info(f'Number of files ingested: {file_count}')
        logging.info(f'Total time taken for data ingestion of {file_count} files is {ingestion_end_time-ingestion_start_time}')

    def ingest_data_from_file(self, file_path, station_id):
        with open(file_path, 'r') as f:
            for line in f:
                data = line.strip().split('\t')

                # Convert the date string to a datetime object
                date = datetime.strptime(data[0], '%Y%m%d').date()

                # Convert temperature and precipitation strings to float in degree Celsius & Millimeter
                max_temp = float(data[1]) / 10 if data[1] != '-9999' else None
                min_temp = float(data[2]) / 10 if data[2] != '-9999' else None
                precipitation = float(data[3]) / 10 if data[3] != '-9999' else None

                # Check if the record already exists in the database to avoid adding duplicate records
                exists = self.db.query(WeatherRecordDB).filter(WeatherRecordDB.station_id == station_id,
                                                               WeatherRecordDB.date == date).first()

                # If the record doesn't exist, create a new WeatherRecordDB object and add it to the session
                if not exists:
                    weather_data = WeatherRecordDB(station_id=station_id, date=date,
                                                   max_temperature=max_temp,
                                                   min_temperature=min_temp,
                                                   precipitation=precipitation
                                                   )
                    self.db.add(weather_data)

            # Commit the changes to the database
            self.db.commit()

    def weather_data_analysis(self):

        # Query to get all the distinct years and weather stations from the database
        year_stations = self.db.query(func.distinct(func.strftime('%Y', WeatherRecordDB.date)),
                                      WeatherRecordDB.station_id).all()

        # Iterate through each year and station to calculate the statistics
        for year, station in year_stations:
            # Query to get all the data for the current year and weather station while ignoring missing values
            data = self.db.query(
                func.avg(WeatherRecordDB.max_temperature),
                func.avg(WeatherRecordDB.min_temperature),
                func.sum(WeatherRecordDB.precipitation)
            ).filter(
                func.strftime('%Y', WeatherRecordDB.date) == year,
                WeatherRecordDB.station_id == station,
                WeatherRecordDB.max_temperature is not None,
                WeatherRecordDB.min_temperature is not None,
                WeatherRecordDB.precipitation is not None
            ).first()

            # Check if the statistics already exist for the year and station, and add them if they don't
            exists = self.db.query(WeatherStatsDB).filter(WeatherStatsDB.station_id == station,
                                                          WeatherStatsDB.year == year).first()

            if not exists:
                insert_into = WeatherStatsDB(station_id=station,
                                             year=year,
                                             avg_max_temperature=data[0],
                                             avg_min_temperature=data[1],
                                             total_precipitation=data[2]
                                             )
                self.db.add(insert_into)
        self.db.commit()

    def get_weather_record(self, station_id, date):
        # Query to get all the data for the specified station_id and year from weather record table
        result = self.db.query(WeatherRecordDB).filter(WeatherRecordDB.station_id == station_id,
                                                       WeatherRecordDB.date == date).all()

        # If there are records, create a list of WeatherStatsItem objects with the retrieved data and returns the list.
        if result:
            results = [WeatherRecordItem(station_id=record.station_id,
                                         date=record.date,
                                         min_temperature=record.min_temperature,
                                         max_temperature=record.max_temperature,
                                         precipitation=record.precipitation) for record in result]
            return results
        else:
            return None

    def get_weather_stats(self, station_id, year):
        # Query to get all the data for the specified station_id and year from weather stats table
        result = self.db.query(WeatherStatsDB).filter(WeatherStatsDB.station_id == station_id,
                                                      WeatherStatsDB.year == year).all()
        # If there are records, create a list of WeatherStatsItem objects with the retrieved data and returns the list.
        if result:
            results = [WeatherStatsItem(station_id=record.station_id,
                                        year=record.year,
                                        avg_min_temperature=record.avg_min_temperature,
                                        avg_max_temperature=record.avg_max_temperature,
                                        total_precipitation=record.total_precipitation) for record in result]
            return results
        else:
            return None
