# Tagup Data Engineer Exercise

## Problem
ExampleCo, Inc is gathering several types of data for its fleet of very expensive machines. They collect four kinds of time series data for each machine in their fleet of very expensive machines. When a machine is operating in normal mode the data behaves in a fairly predictable way, but with a moderate amount of noise. Before a machine fails it will ramp into faulty mode, during which the data appears visibly quite different. Finally, when a machine fails it enters a third, and distinctly different, failed mode where all signals are very close to zero. There are three common sensors associated with each machine. The company has contracted you to take their data extracts (linked below), map the data into your database, and summarize the results and process.

## Assumptions
- This data pipeline is built to serve the purpose of data analytics and machine learning experiments on machine anomaly detection.
- There are three common sensors associated with each machine to collect four kinds of metric data (4 columns in the data). 
	- Sensor_0 -> Column '0'
	- Sensor_1 -> Column '1'
	- Sensor_2 -> Column '2' and Column '3'

## Solution
- <strong>Understand the data</strong>
	- <strong>Data quality</strong>   
	Plot 4 metric values:
	![histogram](/img/histogram.png)
	_All four metric values center around 0, which indicate the machine failed after a short period of normal functioning. There are also some outliers that fall into the ranges of >-200 and >200._
	![scatter](/img/scatter.png)
	_The scatter plots give a better picture of the machine status over the time and the distribution of the outliers._

	- <strong>Database design</strong>  
	Database schema:
	![schema](/img/schema.png)
	Advantages:  
		- This schema fulfills the data analytics purpose by following the STAR schema (OLAP) structure. The fact table _reading_ is associated with three demension tables _machine, sensor, metric_. It has the benefits of STAR schema: easy to understand, flexible to expand, simple to query without complex joins, etc.
		- The (composite) primary key of each table is derived from application data. No surrogate key that adds extra columns to the tables.
		- Necessary index is added in order to improve query performance.

- <strong>Process the data</strong>
	- <strong>Remove invalid data</strong>
		- Null value
		- Invalid data type, e.g. timestamp
	- <strong>Remove outliers</strong>
		- Z score method
	- <strong>Transform the data</strong>
		- Input data:
		![raw](/img/raw.png)
		- Output data:  
		![processed](/img/processed.png)
- <strong>Ingest the data</strong>
	- Choose PostgreSQL for stable performance
	- Use _"INSERT INTO...ON CONFLICT () DO NOTHING"_ query to avoid inserting duplicate records


## Data Pipeline



## How to run

## Required Packages
