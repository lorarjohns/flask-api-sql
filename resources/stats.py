#!/usr/bin/env python

import logging
from flask_jsonpify import jsonify
from flask_restful import Resource
from flask import make_response, request
import os


class Section(Resource):

    def __init__(self, **kwargs):

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG) 
        self.db = kwargs['DataBase']()
        self.query = '''
        SELECT counts.section, COUNT(counts.content_id) as count
        FROM
        (
        SELECT DISTINCT users.user_id, users.content_id, a.section
        FROM users
        JOIN articles a on users.content_id = a.content_id
        WHERE users.user_id=?
        ) AS counts
        GROUP BY counts.section;
        '''

    def get(self):

        '''
        Takes in a user ID `u:1234567`
        returns a JSON object with counts of unique
        articles that user has read
        '''            
        user_id = (request.json['user_id'],)
        
        print(user_id)

        results = self.db.query_db(self.query, user_id)
        tally = {d['section']: d['count'] for d in results}

        return jsonify(tally)

    def post(self):
        return self.get()

if __name__ == "__main__":

    # Local only

    print("stats endpoint")