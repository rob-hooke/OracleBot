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

if __name__ == "__main__":
    create_table()
      