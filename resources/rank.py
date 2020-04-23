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
        user_id = request.json['user_id']
        content_ids = request.json['content_ids']
        
        # How read overall is each article?
        total_pop = self.db.query_db(f'''
                SELECT * FROM (
                SELECT a2.content_id, section, COUNT(*)
                FROM users
                JOIN articles a2 on users.content_id = a2.content_id
                GROUP BY a2.content_id
                ORDER BY COUNT(*) DESC)
                WHERE content_id IN ({', '.join(["'" + id + "'" for id in content_ids])})
                ''')

        overall_pops = {d[0]: d[2] for d in total_pop}
        
        # How much of each section does user read?
        user_data = self.db.query_db(f'''
        SELECT section, COUNT(*)
        FROM users
        JOIN articles a on users.content_id = a.content_id
        WHERE user_id='{user_id}'
        GROUP BY section''')
        individual_pop = {u[0]: u[1]  for u in user_data}
        
        # Which articles has user read?
        read = [i[0] for i in self.db.query_db(f'''
        SELECT users.content_id
        FROM users
        WHERE user_id='{user_id}'
        ''')]
        result = []
        for id in content_ids:
            if id not in read:
                article_topic = self.db.query_db('SELECT section FROM articles WHERE content_id = ?', (id,))[0][0]
                user_pop = individual_pop.get(article_topic, 0)
                tiebreaker = overall_pops.get(id)
                result.append((id, article_topic, user_pop, tiebreaker))
        
        return make_response(jsonify({"content_ids": [item for item in list(zip(*sorted(result, key=lambda x: [x[2], x[3]], reverse=True)))[0]]}))
        
    def sql(self):
        payload = request.json
        user_id = payload['user_id']
        content_ids = payload['content_ids']
	
        query = f'''
        SELECT a.section, a.content_id, user_id,
        RANK() OVER (ORDER BY (
                    SELECT COUNT(a.content_id)
                    OVER (PARTITION BY a.section ORDER BY r.count DESC) AS score
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
        
        return make_response(jsonify({"content_ids": [d["content_id"] for d in user_rank]}))
