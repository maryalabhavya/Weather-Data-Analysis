import os
from datetime import datetime
import logging
import pandas as pd

from app.models.weather_data_model import WeatherRecordDB
from app.db.database_connection import session

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class WeatherService:
    def __init__(self, db=session):
        self.db = db

    def ingest_data(self, data_path):
        for filename in os.listdir(data_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(data_path, filename)

                station_id = filename.split('.')[0]
                self.ingest_data_from_file(file_path=file_path, station_id=station_id)

    def ingest_data_from_file(self, file_path, station_id):
        with open(file_path, 'r') as f:
            for line in f:
                data = line.strip().split('\t')
                date = datetime.strptime(data[0], '%Y%m%d').date()
                max_temp = float(data[1]) / 10 if data[1] != '-9999' else None
                min_temp = float(data[2]) / 10 if data[2] != '-9999' else None
                precipitation = float(data[3]) / 10 if data[3] != '-9999' else None
                exists = self.db.query(WeatherRecordDB).filter(WeatherRecordDB.station_id == station_id,
                                                               WeatherRecordDB.date == date).first()
                if not exists:
                    weather_data = WeatherRecordDB(station_id=station_id, date=date,
                                                   max_temperature=max_temp,
                                                   min_temperature=min_temp,
                                                   precipitation=precipitation
                                                   )
                    self.db.add(weather_data)
            self.db.commit()

        # data = pd.read_csv(file_path, sep="\t", header=None,
        #                    names=['date', 'max_temperature', 'min_temperature', 'precipitation'])
        # # Replace missing values with None
        # data = data.replace(-9999, None)
        # # Parse date string and convert it into datetime.date object
        # data['date'] = data['date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d').date())
        # # Add station ID to data
        # data['station_id'] = station_id
        # # Remove any duplicate rows
        # data.drop_duplicates(inplace=True)
        # data.to_sql('weather_data_record', self.db, if_exists='append', index=False)