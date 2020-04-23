import logging
import os

from flask import make_response, abort, g
from flask import current_app as app

from flask_jsonpify import jsonify
from flask_restful import Resource
from flask import make_response, request
from werkzeug.datastructures import FileStorage

import json
import sqlite3

class Ranker(Resource):

    def __init__(self, **kwargs):

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.db = kwargs['DataBase']()

    def post(self):
        payload = request.json
        user_id = payload['user_id']
        content_ids = payload['content_ids']
	
        query = f'''
        SELECT a.section, content_id, user_id,
        RANK() OVER (ORDER BY (
                    SELECT COUNT(content_id)
                    OVER (PARTITION BY a.section ORDER BY r.count ASC) AS score
                        FROM users
                        )) as rank
        FROM users
        JOIN articles a using (content_id)
        JOIN article_ranks r using (content_id)
        WHERE content_id IN ({', '.join(["'" + id + "'" for id in content_ids])}) AND content_id NOT IN (
                SELECT content_id
                FROM users u
                WHERE user_id='{user_id}'
            )
        GROUP BY content_id
        order by content_id;
        '''
        #For debugging:
        #print(query)
        #print(self.db.db_url)
        user_rank = self.db.query_db(query)
        
        return jsonify({"content_ids": [d["content_id"] for d in user_rank]})
