# US Flight Delay Analysis (2018 - 2025)

##  Project Overview
This project provides an interactive dashboard analyzing US commercial flight delays over a 7-year period (January 2018 to January 2025). The application is built entirely in  **Streamlit** for the frontend and **Pandas/PyArrow** for high-performance data processing.

### Business Logic & Definitions
* **Data Source:** Bureau of Transportation Statistics (BTS) "Marketing Carrier On-Time Performance".
* **Delay Definition:** A flight is considered delayed if it experiences a departure OR arrival difference of **15 minutes or more** from its scheduled time.

## Architecture & Engineering Decisions

Processing 7 years of raw flight data (approximately 85 monthly CSV files, >40 million rows, 15GB+ uncompressed)

To ensure optimal dashboard performance, the data pipeline was split into two distinct phases:
**Extract & Transform (Offline):** A multithreaded Python script was used to download the raw ZIP files, filter strictly for flights meeting the >15m delay criteria, and drop unused columns.
**Data Storage:** Data is stored in the columnar **Parquet** format (`pyarrow` engine) to minimize disk footprint and maximize read speeds.

## Dashboard Features
* **Dynamic Time Zooming:** Users can filter the entire dataset down to specific date ranges.
* **Time Aggregation:** One-click toggling between Weekly, Monthly, Quarterly, and Yearly delay trends.
* **Dimensional Breakdowns:** Interactive visualizations detailing delays by Carrier, Root Cause (Weather, Security, NAS, etc.), Origin City, and Destination City.

## CMD for Running Dash
python -m streamlit run dashboard.py

