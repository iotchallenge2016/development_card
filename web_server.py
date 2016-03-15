from flask import Flask, url_for, request, jsonify, Response
from bson.json_util import dumps
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
	return Response(json.dumps({'Provider' : 'FailSquad'}), mimetype='application/json')

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


@app.route('/sections/<sectionId>', methods = ['GET'])
def api_section(sectionId):
	if request.method == 'GET':
		return Response(dumps(mongo.db.parking.find({'section': sectionId})[0]), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/<sectionId>/free/<quantity>')
def api_section_free(sectionId, quantity, methods = ['GET']):
	if request.method == 'GET':
		quantity = int(quantity)
		data = mongo.db.parking.find({'section': sectionId})[0]
		mongo.db.parking.update_one({'section' : sectionId}, {'$set' : {'spaces' : int(data['spaces'] + quantity)}})
		return Response(dumps(mongo.db.parking.find({'section': sectionId})[0]), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/<sectionId>/reserve/<quantity>')
def api_section_reserve(sectionId, quantity, methods = ['GET']):
	if request.method == 'GET':
		quantity = int(quantity)
		data = mongo.db.parking.find({'section': sectionId})[0]
		if (data['spaces'] > 0):
			mongo.db.parking.update_one({'section' : sectionId}, {'$set' : {'spaces' : int(data['spaces'] - quantity)}})
		return Response(dumps(mongo.db.parking.find({'section': sectionId})[0]), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/add/<sectionId>/<spaces>')
def api_add_section(sectionId, spaces, methods = ['GET']):
	if request.method == 'GET':
		mongo.db.parking.insert_one({'section': sectionId, 'spaces': int(spaces)})
		return Response(dumps({}), status=200, mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/remove/<sectionId>')
def api_remove_section(sectionId, methods = ['GET']):
	if request.method == 'GET':
		result = mongo.db.parking.delete_many({'section': sectionId})
		return Response(dumps({'deleted' : result.deleted_count}), status=200, mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)	

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)