# SurfsUp Data Analysis and API

## Summary
This project contains two main scripts for analyzing weather data and creating a Flask API to serve this data from the `hawaii.sqlite` database. The aim is to evaluate weather patterns and provide accessible endpoints for various weather data queries.

## Objectives
- Perform exploratory data analysis on weather data.
- Develop a Flask API to serve weather data.
- Provide endpoints for precipitation, stations, temperature observations, and temperature statistics.

## Data Description
The dataset includes:
- Measurement IDs
- Station IDs
- Dates
- Precipitation levels
- Temperature observations

## Scripts Included
1. **Weather Data Analysis**: Analyzes the weather data from the `hawaii.sqlite` database.
2. **Weather Data API**: Creates a Flask API to provide weather data endpoints.

## Requirements
- Python 3.10
- pandas module
- matplotlib module
- sqlalchemy module
- flask module

## Instructions

### Weather Data Analysis
1. Ensure `hawaii.sqlite` is in the `Resources` folder.
2. Run the `analysis_script.py` script.

### Weather Data API
1. Ensure `hawaii.sqlite` is in the `Resources` folder.
2. Run the `api_script.py` script.

### Available API Routes
- `/api/v1.0/precipitation`: Returns precipitation data for the last 12 months.
- `/api/v1.0/stations`: Returns a list of weather stations.
- `/api/v1.0/tobs`: Returns temperature observations for the previous year for the most active station.
- `/api/v1.0/YYYY-MM-DD`: Query data for a specific day, format: `YYYY-MM-DD`. Example: `/api/v1.0/2010-01-01`.
- `/api/v1.0/YYYY-MM-DD/YYYY-MM-DD`: Query data for a specific date range, format: `YYYY-MM-DD/YYYY-MM-DD`. Example: `/api/v1.0/2010-01-01/2017-08-23`.

### Note
Ensure the date format follows the `YYYY-MM-DD` pattern for all endpoints.

## Contributions
Contributions are welcome. If you have suggestions or improvements, please open an issue or submit a pull request.
