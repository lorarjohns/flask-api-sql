import logging
from flask_jsonpify import jsonify
from flask_restful import Resource, reqparse, inputs
from flask import make_response

class HealthCheck(Resource):
    def get(self):
        return make_response(
            jsonify({'status': 'OK'}), 200)

    def post(self):
        return make_response(
            jsonify({'status': 'OK'}), 200)
