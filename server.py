from flask import Flask, url_for, request, jsonify, Response, render_template, redirect
from invalid_request import InvalidRequest
from flask.ext.pymongo import PyMongo
from werkzeug import secure_filename
from bson.json_util import dumps
from loader import parse_csv
import json
import os

UPLOAD_FOLDER = os.getcwd() + '/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask('parking-lot', static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongo = PyMongo(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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
 
@app.route('/visualize')
def visualize():
	return render_template('visualizeMode.html')

@app.route('/view', methods=['GET'])
def view_parking_lot():
	data = []
	for result in mongo.db.parking.find():
		data.append(result)
	return render_template('view.html', data=data)

@app.route('/file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            mongo.db.parking.insert_many(json.loads(parse_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))))
	return redirect(url_for('view_parking_lot'))

@app.route('/sections', methods = ['GET'])
def api_sections():
	if request.method == 'GET':
		data = []
		for result in mongo.db.parking.find():
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

@app.route('/sections/<sectionId>/free/<int:quantity>')
def api_section_free(sectionId, quantity, methods = ['GET']):
	if request.method == 'GET':
		data = mongo.db.parking.find({'section': sectionId})[0]
		mongo.db.parking.update_one({'section' : sectionId}, {'$set' : {'capacity' : int(data['capacity'] + quantity)}})
		return Response(dumps(mongo.db.parking.find({'section': sectionId})[0]), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/<sectionId>/reserve/<int:quantity>')
def api_section_reserve(sectionId, quantity, methods = ['GET']):
	if request.method == 'GET':
		data = mongo.db.parking.find({'section': sectionId})[0]
		if (data['capacity'] > 0):
			mongo.db.parking.update_one({'section' : sectionId}, {'$set' : {'capacity' : int(data['capacity'] - quantity)}})
		return Response(dumps(mongo.db.parking.find({'section': sectionId})[0]), mimetype='application/json')
	else:
		raise InvalidUsage('Unsupported Method', 501)

@app.route('/sections/add/<sectionId>/<capacity>')
def api_add_section(sectionId, capacity, methods = ['GET']):
	if request.method == 'GET':
		mongo.db.parking.insert_one({'section': sectionId, 'capacity': int(capacity)})
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