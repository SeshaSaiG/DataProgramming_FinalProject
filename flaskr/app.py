from flask import Flask, render_template, json, template_rendered, Response, Request
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
import pytz
import time
import os
import sys
import json
import schedule
#from flask_apscheduler import APScheduler
 

load_dotenv()

app = Flask(__name__)

#scheduler = APScheduler()

def covidData_serializer(item) -> dict:
    return {
        "id":str(item["_id"]),
        "data":item["data"]
    }

def covidDatas_serializer(items) -> list:
    return [covidData_serializer(item) for item in items]


conn = MongoClient("mongodb+srv://admin:iW70CzDypD5z8Kr5@api.uq5l2w9.mongodb.net/Covid_Data?retryWrites=true&w=majority")
db = conn['Covid_Data']
collection_name = db["Covid_Data"]

# @app.route("/", methods=["GET"])
# def home():
#     return "Welcome"

@app.route("/health", methods=["GET"])
def getHealth():
    data = covidDatas_serializer(db.Cases.find())
    return Response(
            response= json.dumps(data),status=500,mimetype="application/json"
        )

@app.route("/",methods=["GET"])
def getCovidData():
    try:
        data = covidDatas_serializer(db.Cases.find())
        # finalData = Response(
        #     response= json.dumps(data),status=500,mimetype="application/json"
        # )
        print("from html")
        return render_template('index.html', data1 = Response(
            response= json.dumps(data),status=500,mimetype="application/json"
        )
)
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"msg":"Failed to retrive Data"}),status=500,mimetype="application/json"
        )
        

url = "https://covid-19-statistics.p.rapidapi.com/reports"
headers = {
    "X-RapidAPI-Key": "ceba13ce3fmsh54baf7333381a96p1e82f6jsnb4f6c7e0220f",
    "X-RapidAPI-Host": "covid-19-statistics.p.rapidapi.com"
}

provinces = ["California","New York","Texas","Florida","Illinois"]
yesterday = datetime.now() - timedelta(1)
currentDate = str(datetime.strftime(yesterday, '%Y-%m-%d'))

def data_load():
    for x in provinces:
        print(x)
        querystring = {"region_province":x,"iso":"USA","region_name":"US","date":currentDate}
        r = requests.request("GET", url, headers=headers, params=querystring)
        if r.status_code == 200:
            data = r.json()
            collection_name.insert_one(data)

#schedule.every().day.at("14:03").do(data_load)

#def job():
    #print('hello')

#schedule.every(30).seconds.do(job)

# while 1:
#     schedule.run_pending()
#     time.sleep(1)


if __name__ == "__main__":
    #scheduler.add_job(id="test",func = job, trigger = 'interval', seconds = 5)
    app.run(debug=True)
