## Import the required libraries ##
import os
from flask import Flask, abort, jsonify, request, render_template
from flask_cors import CORS 
import json
import pymongo 

import numpy as np
import pandas as pd

import spacy
import en_core_web_sm

import re

import model_script



# connect to the mongoDB cloud
# connection_url='mongodb+srv://abin:dbpassword@cluster0.b8byd.mongodb.net/test?retryWrites=true&w=majority'
connection_url = os.environ.get('MONGODB_URL')

app = Flask(__name__)
client = pymongo.MongoClient(connection_url)

# Access the Database 
Database = client.get_database('Ideapoke') 
# Access the Table 

ReportsTable = Database.Reports

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/getdelay', methods=['POST'])
def get_delay():
    # get the input from the html page
    result=request.form
    
    text=result['text']
    
    mydict=model_script.model_builder(text)
   

    ReportsTable.insert(my_dict)
    
    return render_template('home.html',mydict)
      

if __name__ == '__main__':
    app.run(debug=True)
