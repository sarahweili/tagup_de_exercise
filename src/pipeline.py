#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import glob
import os
from database import *
from processing import process_data




def main():
    # connect to the PostgreSQL server
    params_dic = config()
    conn = connect_to_db(params_dic)
    create_tables(conn)
    
    # map the data into database
    try:
        # read csv file from the path
        for file in glob.glob('../exampleco_data/*.csv'):
            data = pd.read_csv(file)
            # extract file name
            file_name = os.path.basename(file).split('.')[0]
            processed_data = process_data(data, file_name)
            print('\n')
            print('Pre data ingestion:')
            count_records(conn)
            print('\n')
            insert_records(conn, processed_data)
            print('\n')
            print('Post data ingestion:')
            count_records(conn)
            print('\n')
    except IOError:
        print(f"File {file} doesn't exist or isn't readable")
    
    # close the connection to PostgreSQL server
    conn.close()




if __name__ == '__main__':
    main()






