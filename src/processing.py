#!/usr/bin/env python
# coding: utf-8



import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt




def rename_cols(df):
    # rename the timestamp column
    df.rename(columns={df.columns[0]: "date_time" }, inplace = True)
    # rename the metric value columns
    new_names = [(i,'M_'+i) for i in df.iloc[:, 1:].columns.values]
    df.rename(columns = dict(new_names), inplace=True)
    return df




def drop_invalid_data(df):
    # check data type of the timestamp colume
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
    # check data type of metric value columns
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    df = df.dropna(how='any')
    return df




def zscore(df, threshold=3):
    # calculate z score of each metric value column
    df.set_index('date_time', inplace=True)
    z = np.abs(stats.zscore(df))
    df = df[(z < 3).all(axis=1)]
    df.reset_index(inplace=True)
    return df




def transform_df(df, file_name):
    # melt the dataframe
    trans_df = pd.melt(df, id_vars=['date_time'], var_name='metric_name')
    # extract machine_serial_no from the file name
    trans_df['machine_serial_no'] = file_name.split('.')[0]
    # assumption: {'SensorType_0':['Metric_0'], 'SensorType_1':['Metric_1], 'SensorType_2':['Metric_2','Metric_3']}
    trans_df['sensor_type'] = trans_df['metric_name'].apply(lambda x: 'ST_0' if x=='M_0' else ('ST_1' if x=='M_1' else 'ST_2'))
    # generate unique Sensor Serial No
    trans_df['sensor_serial_no'] = trans_df.apply(lambda x: x['machine_serial_no']+ '_'+ x['sensor_type'], axis=1)
    trans_df = trans_df[['sensor_serial_no','sensor_type', 'metric_name','date_time','machine_serial_no','value']]
    return trans_df




def plot_scatter(data):
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize = (20, 5))
    fig.suptitle('Data distribution after removing outliers')
    ax1.scatter(x=range(len(data)), y=data.iloc[:,1])
    ax1.set(title='sensor_0', ylabel='value')
    ax2.scatter(x=range(len(data)), y=data.iloc[:,2])
    ax2.set(title='sensor_1', ylabel='value')
    ax3.scatter(x=range(len(data)), y=data.iloc[:,3])
    ax3.set(title='sensor_2', ylabel='value')
    ax4.scatter(x=range(len(data)), y=data.iloc[:,4])
    ax4.set(title='sensor_3', ylabel='value')
    plt.show()




def process_data(df, file_name):
    data = rename_cols(df)
    valid_data = drop_invalid_data(data)
    clean_data = zscore(valid_data)
    # plot data distribution after removing the outliers
    #plot_scatter(clean_data)
    #print('\n')
    ready_data = transform_df(clean_data, file_name)
    # print output data summary
    print('Data processing completed!')
    print('\n')
    print('Output data information:')
    print(ready_data.info())
    print('\n')
    print('Output data statistics:')
    print(ready_data.describe())
    print('\n')
    return ready_data

