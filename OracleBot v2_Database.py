# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 22:15:32 2019

@author: Boby RObert
"""

import json
import sqlite3
from datetime import datetime

timeframe = '2015-01'
sql_transaction = []
connection = sqlite3.connect('{}.db'.format(timeframe))

c = connection.cursor()

def create_table():
    c.execute("""create table if not exists parent_reply(parent_id text primary key, comment_id text unique, parent text, 
                                                         comment text,subreddit text, unix int, score int)""")
def format_data(data):       # Function to replace Characters
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
        return True


def sql_inser_replace_comment(commentid, parentid, parent,comment,subreddit,time,score):
    try:
        sql = """ update parent_reply set parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? where parent_id =  ?:""".format(parentid,commentid,parent,comment,subreddit,time,score)
        transaction_bldr(sql)
    except Exception as e:
        print('replace comment', str(e))

def sql_insert_has_parent(commentid, parentid, parent,comment, subreddit, time, score):
    try:
        sql = """insert into parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) values ("{}","{}","{}","{}","{}","{}","{}",)""".format(parentid, commentid, parent,comment, subreddit, time, score)
        transaction_bldr(sql)
    except Exception as e:
        print(' ',str(e))

def sql_insert_no_parent(commentid, parentid, comment, subreddit, time, score):
    try:
        sql = """insert into parent_reply (parent_id, comment_id, comment, subreddit, unix, score) values ("{}","{}","{}","{}","{}","{}",)""".format(parentid, commentid, comment, subreddit, time, score)
        transaction_bldr(sql)
    except Exception as e:
        print(' ',str(e))


def transaction_bldr(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        c.execute('begin transaction')
        for s in sql_transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []
    
    

    
if __name__ == "__main__":
    create_table()
    row_counter = 0     #Itertae rows no
    paired_rows = 0
    
    with open("F:/GitHub/OracleBot/RC_2015-01/RC_{}".format(timeframe), buffering = 1000) as f:
        for row in f:
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            comment_id = row['name']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            parent_data = find_parent(parent_id)
            
            if score >= 2:
                if acceptable(body):
                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score:
                        if score > existing_comment_score:
                            sql_inser_replace_comment(comment_id, parent_id, parent_data ,body, subreddit, created_utc, score)
                            
                    else:
                        if parent_data:
                            sql_insert_has_parent(comment_id, parent_id, parent_data, body, subreddit, created_utc, score)
                            paired_rows += 1
                        else:
                            sql_insert_no_parent(comment_id, parent_id, body, subreddit, created_utc, score)
                            
            if row_counter % 100000 == 0:
                print("Total rows read: {}. paired rows: {}, time: {}".format(row_counter, paired_rows, str(datetime.now)))