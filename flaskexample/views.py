#this uses cached results to return 3 sets of tables to the user depending on the age group they select

import sys
sys.path.append("flaskexample")

from flask import render_template
from flask import request
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
username = 'shawnramirez'
engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))


#-- Homepage
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Better Screen Time', user = { 'nickname': 'shawnramirez' })


#-- Output to User
@app.route('/output', methods=['GET', 'POST'])
def output():
    con = None
    con = psycopg2.connect(database = dbname, user = username)

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
        query_results = pd.read_sql_query(sql_query,con)

        for i in range(0,query_results.shape[0]):
            user_results.append(dict(title=query_results.iloc[i]['title'],
                                 url=query_results.iloc[i]['url'],
                                 description=query_results.iloc[i]['description'],
                               thumbnail=query_results.iloc[i]['thumbnail']))


    con.close()

    return render_template("output.html", results = user_results, error_message = error_message)
