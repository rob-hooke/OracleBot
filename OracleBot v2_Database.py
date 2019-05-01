# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 22:15:32 2019

@author: Boby RObert
"""

import json
import sqlite3
from datetime import datetime

timeframe = '2015-05'
sql_transaction = []

connection = sqlite3.connect('{}.db'.format(timeframe))

c = connection.cursor()

def create_table():
    c.execute("""create table if not exists parent_reply(parent_id text primary key, comment_id text unique, parent text, 
                                                         comment text,subreddit text, unix int, score int)""")
def format(data):       # Function to replace Characters
    data = data.replace("\n"," newlinechar ").replace("\r"," newlinechar ").replace('"',"'")
    return data
def find_existing_score(pid):
    try:
        sql = "select score from parent_reply where parent_id = '{}' limit 1".format(pid)
        c.execute(sql)
        result =  c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        return False
    
def find_parent(pid):       #Function to store parent ID
    try:
        sql = "select comment from parent_reply where comment_id = '{}' limit 1".format(pid)
        c.execute(sql)
        result =  c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        return False

def acceptable(data):
    if len(data.split(' ')) > 50 or len(data) < 1:
        return False
    elif len(data) > 1000:
        return False
    elif data == '[deleted]' or data == '[removed]':
        return False
    else:
        return False
    
if __name__ == "__main__":
    create_table()
    row_counter = 0     #Itertae rows no
    paired_rows = 0
    
    with open("F:/.../{}/RC_{}".format(timeframe.split('-')[0], timeframe), buffering = 1000) as f:
        for row in f:
            row+counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            parent_data = find_parent(parent_id)
            
            if score >= 2:
                existing_comment_score = find_existing_score(parent_id)
                if existing_comment_score:
                    if score > existing_comment_score:
                        