from flask import Flask, url_for, request, jsonify, Response, render_template, redirect
from invalid_request import InvalidRequest
from flask.ext.pymongo import PyMongo
from flask.ext.autodoc import Autodoc
from werkzeug import secure_filename
from time import gmtime, strftime
from bson.json_util import dumps
from loader import parse_csv
from graph import Graph
import pymongo
import json
import os

UPLOAD_FOLDER = os.getcwd() + '/uploads'
COLLECTION = 'itesm'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask('parking-lot', static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo = PyMongo(app)
auto = Autodoc(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_sections():
	data = []
	for result in mongo.db[COLLECTION].find({'section' : {'$exists': True}}).sort('capacity', pymongo.DESCENDING):
		data.append(result)
	return data

def get_places():
	data = []
	for result in mongo.db[COLLECTION].find({'place' : {'$exists': True}}):
		data.append(result)
	return data

def get_graph():
	return Graph(get_places(), get_sections())

@app.errorhandler(InvalidRequest)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route('/')
@auto.doc(groups=['admin','users'])
def root():
	"""Returns the Homepage"""
	return render_template('index.html')

@app.route('/about')
@auto.doc(groups=['admin','users'])
def about():
	"""Returns the 'About Us' page"""
	return render_template('about.html')

@app.route('/view', methods=['GET'])
@auto.doc(groups=['admin','users'])
def view_parking_lot():
	"""Returns the Parking Lot Visualizer"""
	return render_template('view.html', data=get_sections())

@app.route('/file', methods=['POST'])
@auto.doc(groups=['admin'])
def upload_file():
	"""Lets you upload a csv file to be parsed and inserted into the database"""
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			mongo.db[COLLECTION].insert_many(json.loads(parse_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))))
	return redirect(url_for('view_parking_lot'))

@app.route('/graph')
@auto.doc(groups=['admin'])
def api_graph_json():
	"""Returns the representation of a graph as a JSON"""
	return Response(dumps(get_graph().to_dict()), mimetype='application/json')

@app.route('/graph_text')
@auto.doc(groups=['admin'])
def api_graph_text():
	"""Returns the representation of the graph as text"""
	return get_graph().html_text()

@app.route('/graph/closest_parking_section_for/<dstId>')
@auto.doc(groups=['admin'])
def api_graph_closest_parking_section_for(dstId):
	"""Returns the closest parking area to the destionation zone"""
	g = get_graph()
	return Response(dumps(g.find_section(g.get_closest_parking_section(dstId))), mimetype='application/json')

@app.route('/graph/save')
@app.route('/graph/save/<collection>')
@auto.doc(groups=['admin'])
def api_graph_save(collection='graphDB'):
	"""Saves the graph into the specified collection"""
	g = get_graph()
	to_insert = g.to_dict()
	to_insert['createdAt'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	mongo.db[collection].insert_one(to_insert)
	return Response(dumps(to_insert), mimetype='application/json')

@app.route('/sections', methods = ['GET'])
@auto.doc(groups=['admin'])
def api_sections():
	"""Returns the sections as a JSON representation"""
	if request.method == 'GET':
		return Response(dumps(get_sections()), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/<sectionId>', methods = ['GET'])
@auto.doc(groups=['admin'])
def api_section(sectionId):
	"""Returns the section of the given *sectionId as a JSON representation"""
	if request.method == 'GET':
		return Response(dumps(mongo.db[COLLECTION].find({'section': sectionId})[0]), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/<sectionId>/free/<int:quantity>')
@auto.doc(groups=['admin'])
def api_section_free(sectionId, quantity, methods = ['GET']):
	"""Frees the *quantity of spaces defined from the specified *sectionId, returns the updated section a JSON representation"""
	if request.method == 'GET':
		data = mongo.db[COLLECTION].find({'section': sectionId})[0]
		if data['capacity'] + quantity < data['max']:
			mongo.db[COLLECTION].update_one({'section' : sectionId}, {'$inc' : {'capacity' : quantity}})
		return Response(dumps(mongo.db[COLLECTION].find({'section': sectionId})[0]), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/<sectionId>/reserve/<int:quantity>')
@auto.doc(groups=['admin'])
def api_section_reserve(sectionId, quantity, methods = ['GET']):
	"""Reserves the *quantity of spaces defined from the specified *sectionId, returns the updated section a JSON representation"""
	if request.method == 'GET':
		data = mongo.db[COLLECTION].find({'section': sectionId})[0]
		if (data['capacity'] > 0 and data['capacity'] + quantity < data['max']):
			mongo.db[COLLECTION].update_one({'section' : sectionId}, {'$inc' : {'capacity' :  -quantity}})
		return Response(dumps(mongo.db[COLLECTION].find({'section': sectionId})[0]), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/add/<sectionId>/<int:capacity>')
@auto.doc(groups=['admin'])
def api_add_section(sectionId, capacity, methods = ['GET']):
	"""Adds a new section with the specified *sectionId and the number of *capacity* as free spaces"""
	if request.method == 'GET':
		mongo.db[COLLECTION].insert_one({'section': sectionId, 'capacity': capacity, "max" : capacity})
		return Response(dumps({}), status=200, mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/remove/<sectionId>')
@auto.doc(groups=['admin'])
def api_remove_section(sectionId, methods = ['GET']):
	"""Removes the specified section from the parking lot"""
	if request.method == 'GET':
		result = mongo.db[COLLECTION].delete_many({'section': sectionId})
		return Response(dumps({'deleted' : result.deleted_count}), status=200, mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)	

@app.route('/places', methods = ['GET'])
@auto.doc(groups=['admin'])
def api_places():
	"""Returns the reachable places from the parking lot as a JSON representation"""
	if request.method == 'GET':
		return Response(dumps(get_places()), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/spec')
@auto.doc(groups=['users','admin'])
def documentation():
	"""Returns the documentation"""
	return auto.html(groups=['admin', 'users'], template="doc.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)