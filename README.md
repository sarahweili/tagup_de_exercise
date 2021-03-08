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
- Understand the data
	- Data quality
	Plot 4 metric values:
	![histogram](/img/histogram.png)
	![scatter](/img/scatter.png)


	- Database design
- Process the data
- Ingest the data


## Data Pipeline


## How to run

## Required Packages
