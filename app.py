import os
import logging

from flask import Flask
from flask import g
from flask_restful import Api, Resource
import sqlite3

from resources import healthcheck, rank, stats

logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

basedir = os.path.abspath(os.path.dirname(__file__))

class DataBase:
    def __init__(self):
        self.db_url = os.path.join(app.root_path, 'rank_data.db')
        self.db = sqlite3.connect(self.db_url)
        self.db.row_factory = self.dict_factory

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_db(self):
        #db = getattr(g, '_database', None)
        if self.db is None:
            self.db = sqlite3.connect(self.db_url)
            #db = g._database = sqlite3.connect(self.db_url)

    def query_db(self, query, args=(), one=False):
        cur = self.db.execute(query, args)
        print(cur)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

class HelloNYT(Resource):
    def get(self):
        return "Hello!"

api.add_resource(HelloNYT, '/')
api.add_resource(healthcheck.HealthCheck, '/healthcheck', methods=['GET'])
api.add_resource(stats.Section, '/stats/section', methods=['GET'], resource_class_kwargs={'DataBase': DataBase})
api.add_resource(rank.Ranker, '/rank/section', methods=['POST'], resource_class_kwargs={'DataBase': DataBase})
logger.info("App initialized.")

if __name__ == '__main__':
    logger.info("Starting app.")
    app.run(host='0.0.0.0', port=5000,
            debug=True) # Debug enabled for dev only