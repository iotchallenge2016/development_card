from flask import jsonify

class InvalidRequest(Exception):
	status_code = None
	message = None
	payload = None

	def __init__(self, message, status_code, payload=None):
		Exception.__init__(self)
		self.message = message
		self.status_code = status_code
		self.payload = payload

	def to_dic(self):
		rv = dict(self.payload or ())
		rv['message'] = self.message
		return rv