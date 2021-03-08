#!/usr/bin/env python
# coding: utf-8



import sys
import psycopg2
from configparser import ConfigParser
import pandas as pd




def config(filename='config.ini', section='postgresql'):
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filenmae} file')

    return db


# In[195]:


def connect_to_db(params_dic):
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        sys.exit(1) 
    print("Connection was established successfully!")
    print('\n')
    return conn




def create_tables(conn):
    queries = (
    """
    CREATE TABLE metric (
        metric_name VARCHAR(255) PRIMARY KEY,
        description TEXT
    )
    """,
    """ 
    CREATE TABLE machine (
        machine_serial_no VARCHAR(255) PRIMARY KEY,
        machine_type VARCHAR(255)
    )
    """,
    """
    CREATE TABLE sensor (
        sensor_serial_no VARCHAR(255) PRIMARY KEY,
        sensor_type VARCHAR(255) NOT NULL
    )
    """,
    """
    CREATE TABLE reading (
        sensor_serial_no VARCHAR(255),
        metric_name VARCHAR(255),
        date_time TIMESTAMP,
        machine_serial_no VARCHAR(255) NOT NULL,
        value REAL NOT NULL,
        PRIMARY KEY (sensor_serial_no, metric_name, date_time),
        FOREIGN KEY (sensor_serial_no)
            REFERENCES sensor (sensor_serial_no),
        FOREIGN KEY (metric_name)
            REFERENCES metric (metric_name),
        FOREIGN KEY (machine_serial_no)
            REFERENCES machine (machine_serial_no)
    )
    """,
    """
    CREATE INDEX machine_idx ON reading (machine_serial_no)
    """
    )
    
    cursor = conn.cursor()
    try:
        for query in queries:
            cursor.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
        cursor.close()
        return 1
    print("Tables were created successfully!")
    print('\n')
    cursor.close()
    




def count_records(conn):
    # count row no in tables
    queries = (
    'SELECT COUNT(*) FROM sensor',
    'SELECT COUNT(*) FROM machine',
    'SELECT COUNT(*) FROM metric',
    'SELECT COUNT(*) FROM reading'
    )
    
    cursor = conn.cursor()
    results = []
    try:
        for query in queries:
            cursor.execute(query)
            results.append(cursor.fetchone())
        print('Table sensor contains ', results[0][0], ' rows')
        print('Table machine contains ', results[1][0], ' rows')
        print('Table metric contains ', results[2][0], ' rows')
        print('Table reading contains ', results[3][0], ' rows')
        print('\n')
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()




def insert_records(conn, df):
    # place-holders for machine(machine_type) and metric(description) attributes
    df['machine_type'] = 'Null'
    df['description'] = 'Null'
    
    # only insert records that don't exist in the tables
    queries = (
    f"""
    INSERT INTO sensor (sensor_serial_no, sensor_type)
    VALUES {','.join([str(i) for i in list(df[['sensor_serial_no', 'sensor_type']].to_records(index=False))])}
    ON CONFLICT (sensor_serial_no)
    DO NOTHING
    """,
    
    f"""
    INSERT INTO machine (machine_serial_no, machine_type)
    VALUES {','.join([str(i) for i in list(df[['machine_serial_no', 'machine_type']].to_records(index=False))])}
    ON CONFLICT (machine_serial_no)
    DO NOTHING
    """,
    
    f"""
    INSERT INTO metric (metric_name, description)
    VALUES {','.join([str(i) for i in list(df[['metric_name', 'description']].to_records(index=False))])}
    ON CONFLICT (metric_name)
    DO NOTHING
    """,
    
    f"""
    INSERT INTO reading (sensor_serial_no, metric_name, date_time, machine_serial_no, value)
    VALUES {','.join([str(i) for i in list(df[['sensor_serial_no', 'metric_name', 'date_time', 'machine_serial_no', 'value']].to_records(index=False))])}
    ON CONFLICT (sensor_serial_no, metric_name, date_time)
    DO NOTHING
    """
    )
    
    cursor = conn.cursor()
    try:
        for query in queries:
            cursor.execute(query)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        conn.rollback()
        cursor.close()
        return 1
    print("Records were inserted successfully!")
    print('\n')
    cursor.close()






