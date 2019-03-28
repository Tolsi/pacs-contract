import json

import requests

import sys

from dateutil import tz

sys.path.append('../sample')

from serialize_image import serialize_image
from flask import Flask, request, jsonify
import dataset
from datetime import timedelta


db = dataset.connect('sqlite:///db.sqlite')
employees_table = db['employees']
marks_table = db['marks']

from datetime import datetime

CONTRACT_ID = "H7XhErK1YzmY2i1EzNpfcSZv44vEFQGKLa89gUjsi15"
SENDER = "3N2ALKEtTHj2WBCxrmnCgBrf1AoTuv84bbF"
CALL_CONTRACT_NODE_URL = 'http://localhost:6862/contracts/execute'
APIKEY = 'vostok'

def mark_image(image_base64):
    r = requests.post(CALL_CONTRACT_NODE_URL, json={
        "contractId": CONTRACT_ID,
        "fee": 10000000,
        "sender": SENDER,
        "type": 104,
        "version": 1,
        "params":[
            {"key": "cmd", "value": "MARK", "type": "string"},
            {"key": "photo", "value": image_base64, "type": "binary"}
        ]
    }, headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-API-Key': APIKEY})
    if r.status_code != 200:
        raise ValueError("Bad request: " + r.text)

def register_face(name, details, image_base64):
    r = requests.post(CALL_CONTRACT_NODE_URL, json={
        "contractId": CONTRACT_ID,
        "fee": 10000000,
        "sender": SENDER,
        "type": 104,
        "version": 1,
        "params":[
            {"key": "cmd", "value": "ADD", "type": "string"},
            {"key": "photo", "value": image_base64, "type": "binary"},
            {"key": "name", "value": name, "type": "string"},
            {"key": "details", "value": details, "type": "string"}
        ]
    }, headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-API-Key': APIKEY})
    if r.status_code != 200:
        raise ValueError("Bad request: " + r.text)

app = Flask(__name__)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    req = request.get_json()
    if 'name' not in req or 'description' not in req or 'photo' not in req:
        return 'json object should contains \'name\', \'description\' and \'photo\' fields', 400
    try:
        register_face(req['name'], req['description'], req['photo'])
        return jsonify(success=True)
    except:
        return jsonify(success=False)

@app.route('/mark_employee', methods=['POST'])
def mark_employee():
    req = request.get_json()
    if 'photo' not in req:
        return 'json object should contains \'photo\' field', 400
    try:
        mark_image(req['photo'])
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False)

@app.route('/employees_by_day')
def employees_by_day():
    date = request.args.get('date')
    if date is None:
        query_datetime = datetime.now()
    else:
        query_datetime = datetime.strptime(date, '%Y-%m-%d')

    start = datetime(query_datetime.year, query_datetime.month, query_datetime.day, tzinfo=tz.tzutc()).astimezone(tz.gettz('Europe/Moscow'))
    end = start + timedelta(1)
    result = list(db.query('SELECT q.ts, q.mark_photo, e.name, e.details, e.photo FROM (SELECT CAST(strftime(\'%s\', i) AS INT) AS ts, employee, mark_photo FROM (SELECT m.id AS i, m.mark_photo AS mark_photo, j.value AS employee FROM marks AS m CROSS JOIN json_each(m.employees) AS j where m.id between date(:from) and date(:to)) GROUP BY employee) AS q LEFT JOIN employees AS e ON q.employee == e.id;', {'from': start, 'to': end}))

    return jsonify(result)

@app.route('/all_employees')
def all_employees():
    return jsonify(list(db.query('SELECT name, details, photo FROM employees')))

app.run(port=5010)