## Import the required libraries ##
import os
from flask import Flask, abort, jsonify, request, render_template
from flask_cors import CORS 
import json
import pymongo 

import numpy as np
import pandas as pd

import spacy
import re
# Script file to create entity and preprocess
import model_script

model='en_core_web_sm'

# connect to the mongoDB cloud
# connection_url='mongodb+srv://abin:dbpassword@cluster0.b8byd.mongodb.net/test?retryWrites=true&w=majority'
connection_url = os.environ.get('MONGODB_URL')

## Instantiate the app
app = Flask(__name__)

# Connect to mongodb 
client = pymongo.MongoClient(connection_url)

# Access the Database 
Database = client.get_database('Ideapoke') 

# Access the Table 
ReportsTable = Database.Reports

# Decorator to route the home page
@app.route('/')
def home():
    return render_template('home.html')

# Decorator to retun the result page
@app.route('/getdelay', methods=['POST'])
def get_delay():
    # get the input from the html page
    result=request.form
    
    text=result['text']
    
    # Pass the input and get the output
    mydict=model_script.model_builder(text,model)
    
    # Create a dataframe to capture the input & output
    Output=pd.DataFrame({'Input':str(text),'Output':mydict})
    
    # Store the output in the database
    ReportsTable.insert(Output)
        
    return render_template('result.html',user_data=mydict)
      

if __name__ == '__main__':
    app.run(debug=True)
