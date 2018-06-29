#this uses cached results to return 3 sets of tables to the user depending on the age group they select

import sys
sys.path.append("flaskexample")

from flask import render_template
from flask import request
from flask import g

#from flask import jsonify

from flaskexample import app
#from flaskexample import ytgetter
#from flaskexample import wordplay
#from flaskexample import model

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

import pandas as pd
import numpy as np
#import json
#import pickle

#from sklearn.preprocessing import normalize
#from sklearn.decomposition import TruncatedSVD
#from sklearn.linear_model import LogisticRegression
#from numpy import inf



#-- Set up postgre
dbname = 'bst'
username = 'ubuntu'
host = 'localhost'
engine = create_engine('postgres://%s%s/%s'%(username,host,dbname))
con = None
#con = psycopg2.connect(database=dbname, user=username)
def old_get_db():
    global con
    if con is None:
        con = psycopg2.connect(database=dbname, user=username, host=host, password='bst29')
    return con

def get_db():
    if not hasattr(g, 'db_conn'):
        g.db_conn = psycopg2.connect(database=dbname, user=username, host=host, password='bst29')
    return g.db_conn

#con = psycopg2.connect("dbname='bst' user='ubuntu' host='localhost' password='bst29'")

#-- Homepage
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Better Screen Time', user = { 'nickname': 'ubuntu' })


#-- Output to User
@app.route('/output', methods=['GET', 'POST'])
def output():
    #con = None
    #con = psycopg2.connect(database = dbname, user = username,port=5432)

    # get user 'query' from input field
    query=request.form.get('query')
    # get age group
    agerange=request.form.get('agerange')

    user_results = []

    if query == '':
        error_message = "Please type in your search."
    else:
        error_message = ''
        ### using cached results table
        sql_query = """
        SELECT * FROM results_table WHERE (predage=%s AND query='%s') ORDER BY match;
        """% (agerange, query) #
        query_results = pd.read_sql_query(sql_query,get_db())

        for i in range(0,query_results.shape[0]):
            user_results.append(dict(title=query_results.iloc[i]['title'],
                                 url=query_results.iloc[i]['url'],
                                 description=query_results.iloc[i]['description'],
                               thumbnail=query_results.iloc[i]['thumbnail']))

            #    con.close()
    return render_template("output.html", results = user_results, error_message = error_message)

@app.teardown_appcontext
def teardown_db(error):
    if hasattr(g,'db_conn'):
        print('ON VA FERMER')
        g.db_conn.close()
        g.pop('db_conn', None)
