from flask import Flask, url_for, request, jsonify, Response, render_template, redirect
from invalid_request import InvalidRequest
from flask.ext.pymongo import PyMongo
from werkzeug import secure_filename
from bson.json_util import dumps
from loader import parse_csv
from graph import Graph
import json
import os

UPLOAD_FOLDER = os.getcwd() + '/uploads'
COLLECTION = 'itesm'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask('parking-lot', static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo = PyMongo(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_sections():
	data = []
	for result in mongo.db[COLLECTION].find({'section' : {'$exists': True}}):
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
def root():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/view', methods=['GET'])
def view_parking_lot():
	data = []
	return render_template('view.html', data=get_sections())

@app.route('/file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            mongo.db[COLLECTION].insert_many(json.loads(parse_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))))
	return redirect(url_for('view_parking_lot'))

@app.route('/graph')
def api_print_graph():
	return get_graph().html_text()

@app.route('/graph/<dstId>')
def api_graph_closest_parking_zone(dstId):
	g = get_graph()
	return Response(dumps(g.find_section(g.get_closest_parking_section(dstId))), mimetype="application/json")

@app.route('/sections', methods = ['GET'])
def api_sections():
	if request.method == 'GET':
		return Response(dumps(get_sections()), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/<sectionId>', methods = ['GET'])
def api_section(sectionId):
	if request.method == 'GET':
		return Response(dumps(mongo.db[COLLECTION].find({'section': sectionId})[0]), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/<sectionId>/free/<int:quantity>')
def api_section_free(sectionId, quantity, methods = ['GET']):
	if request.method == 'GET':
		data = mongo.db[COLLECTION].find({'section': sectionId})[0]
		if data['capacity'] + quantity < data['max']:
			mongo.db[COLLECTION].update_one({'section' : sectionId}, {'$inc' : {'capacity' : quantity}})
		return Response(dumps(mongo.db[COLLECTION].find({'section': sectionId})[0]), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/<sectionId>/reserve/<int:quantity>')
def api_section_reserve(sectionId, quantity, methods = ['GET']):
	if request.method == 'GET':
		data = mongo.db[COLLECTION].find({'section': sectionId})[0]
		if (data['capacity'] > 0):
			mongo.db[COLLECTION].update_one({'section' : sectionId}, {'$inc' : {'capacity' :  -quantity}})
		return Response(dumps(mongo.db[COLLECTION].find({'section': sectionId})[0]), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/add/<sectionId>/<int:capacity>')
def api_add_section(sectionId, capacity, methods = ['GET']):
	if request.method == 'GET':
		mongo.db[COLLECTION].insert_one({'section': sectionId, 'capacity': capacity, "max" : capacity})
		return Response(dumps({}), status=200, mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/remove/<sectionId>')
def api_remove_section(sectionId, methods = ['GET']):
	if request.method == 'GET':
		result = mongo.db[COLLECTION].delete_many({'section': sectionId})
		return Response(dumps({'deleted' : result.deleted_count}), status=200, mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)	

@app.route('/places', methods = ['GET'])
def api_places():
	if request.method == 'GET':
		return Response(dumps(get_places()), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)