# Weather-Data-Analysis

This project involves designing a database model, ingesting weather data from raw text files, performing data analysis, and creating a REST API.

**Weather Data Description**

The wx_data directory has files containing weather data records from 1985-01-01 to 2014-12-31. Each file corresponds to a particular weather station from Nebraska, Iowa, Illinois, Indiana, or Ohio.

Each line in the file contains 4 records separated by tabs:

1. The date (YYYYMMDD format)
2. The maximum temperature for that day (in tenths of a degree Celsius)
3. The minimum temperature for that day (in tenths of a degree Celsius)
4. The amount of precipitation for that day (in tenths of a millimeter)

Missing values are indicated by the value -9999.

**1. Data Modeling:**

The chosen database is SQLite. The data model to represent the weather data records is defined in SQLAlchemy data definition format.

**2. Data Ingestion**

The code to ingest weather data from raw text files into the database is provided in app/service/weather_data_service.py. The ingest_data() function reads the text files line by line, parses the records, and inserts them into the database.

**3. Data Analysis**

The code used to calculate the weather statistic values and store them in the database is provided in app/service/weather_data_service.py.  The weather_data_analysis() function queries the WeatherData table for the data, performs the calculations for each year and station, and inserts the results into the WeatherStats table.

**4. REST API:**

FastAPI is chosen as the web framework for this project. Two GET endpoints are created: /api/weather and /api/weather/stats. Both endpoints return a JSON-formatted response with a representation of the ingested/calculated data in the database. Clients can filter the response by date and station ID using the query string, and data is paginated.

The Swagger/OpenAPI endpoint is provided at /docs.

All necessary files to run the API locally, along with unit tests, are provided in the app directory. The main file to run the API is main.py.

**To run the API, follow these steps:**

1. Install the required packages by running pip install -r requirements.txt.
2. Run python main.py to start the API or run `uvicorn main:api --reload` in the terminal
3. Open your web browser and go to http://localhost:8000/docs to access the Swagger/OpenAPI endpoint and test the API.