from flask import Flask, url_for, request, jsonify, Response
from bson.json_util import dumps, loads
from invalid_request import InvalidRequest
from flask.ext.pymongo import PyMongo
import json
app = Flask('parking-lot')
mongo = PyMongo(app)

@app.errorhandler(InvalidRequest)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route('/')
def root():
	print mongo.db.parking.find({})
	return Response(json.dumps({'failSquad' : True}), mimetype='application/json')

@app.route('/sections', methods = ['GET'])
def api_sections():
	if request.method == 'GET':
		resultSet = mongo.db.parking.find()
		data = []
		for result in resultSet:
			data.append(result)
		return Response(dumps(data), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)


@app.route('/sections/<sectionId>', methods = ['GET', 'POST'])
def api_section(sectionId):
	data = []
	for result in mongo.db.parking.find({'section': sectionId}):
		data.append(result)
	if request.method == 'GET':
		return Response(dumps(data), mimetype='application/json')
	elif request.method == 'POST':
		if (request.headers['Content-Type'] == 'application/json'):
			print 'JSON POSTING'
			result = loads(data)
			print json.loads(request.json)
			updateResult = mongo.db.parking.update_one({'section': sectionId}, {'space', str(int(2) - 1)})
			return Response(dumps(updateResult), mimetype='application/json')
		else:
			raise InvalidUsage('Unsupported Content-Type', 501)
	else:
		raise InvalidUsage('Unsupported Method', 501)



if __name__ == '__main__':
    app.run(host='0.0.0.0')