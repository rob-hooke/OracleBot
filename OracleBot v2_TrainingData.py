# -*- coding: utf-8 -*-
"""
Created on Thu May  2 22:31:14 2019

@author: Boby Robert
"""

import sqlite3
import pandas as pd

timeframes = ['2015-05']

for timeframe in timeframes:
    connection =  sqlite3.connect('2015-05.db'.format(timeframe))
    c = connection.cursor()
    limit = 5000    #No of data fethed from sql db
    last_unix = 0   #help in buffer through database
    cur_length = limit
    counter = 0
    test_done = False
    while cur_length == limit:
        df = pd.read_sql("select * from parent_reply where unix > {} and parent not null and score > 0 order by unix asc limit {}".format(last_unix, limit), connection)
        last_unix = df.tail(1)['unix'].values[0]
        cur_length = len(df)
        if not test_done:           #initial 5000 for testng model
            with open("test.from",'a', encoding = 'utf8') as f:
                for content in df['parent'].values:
                    f.write(content+'\n')
            with open("test.to",'a', encoding = 'utf8') as f:
                for content in df['comment'].values:
                    f.write(content+'\n')

            test_done = True        # Test dataset file done
        else:                       # Subsequent 5000 are appended for training model
            with open("train.from",'a', encoding = 'utf8') as f:
                for content in df['parent'].values:
                    f.write(content+'\n')
            with open("train.to",'a', encoding = 'utf8') as f:
                for content in df['comment'].values:
                    f.write(content+'\n')
        
        counter += 1
        if counter % 20 == 0:
            print(counter*limit, 'rows completed')
        