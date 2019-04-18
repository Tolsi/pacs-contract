import json

import requests

import sys

from dateutil import tz

sys.path.append('../sample')

from serialize_image import serialize_image
from flask import Flask, request, jsonify
import dataset
from datetime import timedelta

from datetime import datetime

from flask_cors import CORS, cross_origin

CONTRACT_ID = "GPnVdqACjSo4wevbRioCVMAa1guwMyABqEeBxbzxkAFE"
SENDER = "3N2ALKEtTHj2WBCxrmnCgBrf1AoTuv84bbF"
CALL_CONTRACT_NODE_URL = 'http://localhost:6862/transactions/sign'
APIKEY = 'vostok'

def mark_image(image_base64):
    r = requests.post(CALL_CONTRACT_NODE_URL, json={
	    "broadcast": True,
		"type": 104,
        "contractId": CONTRACT_ID,
        "fee": 15000000,
        "sender": SENDER,
        "type": 104,
        "version": 1,
        "params":[
            {"key": "cmd", "value": "MARK", "type": "string"},
            {"key": "photo", "value": image_base64, "type": "binary"}
        ]
    }, headers={'content-type': 'application/json', 'X-API-Key': 'vostok'})
    if r.status_code != 200:
        raise ValueError("Bad request: " + r.text)

def register_face(name, details, image_base64):
    r = requests.post(CALL_CONTRACT_NODE_URL, json={
        "broadcast": True,
		"type": 104,
		"contractId": CONTRACT_ID,
        "fee": 15000000,
        "sender": SENDER,
        "type": 104,
        "version": 1,
        "params":[
            {"key": "cmd", "value": "ADD", "type": "string"},
            {"key": "photo", "value": image_base64, "type": "binary"},
            {"key": "name", "value": name, "type": "string"},
            {"key": "details", "value": details, "type": "string"}
        ]
    }, headers={'content-type': 'application/json', 'X-API-Key': 'vostok'})
    if r.status_code != 200:
        raise ValueError("Bad request: " + r.text)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/add_employee', methods=['POST'])
@cross_origin()
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
@cross_origin()
def mark_employee():
    req = request.get_json()
    if 'photo' not in req:
        return 'json object should contains \'photo\' field', 400
    try:
        mark_image(req['photo'])
        return jsonify(success=True)
    except Exception as e:
        print(e)
        return jsonify(success=False)

@app.route('/employees_by_day')
@cross_origin()
def employees_by_day():
	with dataset.connect('sqlite:///db.sqlite') as db:
		date = request.args.get('date')
		if date is None:
			query_datetime = datetime.now()
		else:
			query_datetime = datetime.strptime(date, '%Y-%m-%d')

		start = datetime(query_datetime.year, query_datetime.month, query_datetime.day, tzinfo=tz.tzutc()).astimezone(tz.gettz('Europe/Moscow'))
		end = start + timedelta(1)
		results = list(db.query('SELECT q.ts, q.mark_photos, e.name, e.details, e.photo FROM (SELECT json_group_array(CAST(strftime(\'%s\', i) AS INT)) AS ts, json_group_array(mark_photo) as mark_photos, employee FROM (SELECT m.id AS i, m.mark_photo AS mark_photo, j.value AS employee FROM marks AS m CROSS JOIN json_each(m.employees) AS j where m.id between date(:from) and date(:to)) GROUP BY employee) AS q JOIN employees AS e ON q.employee == e.id;', {'from': start, 'to': end}))

		def handle_json_fields(res):
			res['ts'] = json.loads(res['ts'])
			res['mark_photos'] = json.loads(res['mark_photos'])
			return res

		return jsonify([handle_json_fields(result) for result in results])

@app.route('/all_employees')
@cross_origin()
def all_employees():
	with dataset.connect('sqlite:///db.sqlite') as db:
		return jsonify(list(db.query('SELECT name, details, photo FROM employees')))

app.run(host='0.0.0.0', port=5010)