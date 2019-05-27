#!/usr/bin/env python3
import json

import flask
import peewee
from flask import request
from peewee import Model, BigIntegerField, CharField
from playhouse.shortcuts import model_to_dict

from Util import getCurrentTimeMillis

app = flask.Flask(__name__)
#app.config["DEBUG"] = True
db = peewee.SqliteDatabase('elastic-archiver.db')


class BaseModel(Model):
    class Meta:
        database = db


class ElasticServer(BaseModel):
    id = BigIntegerField(primary_key=True, unique=True)
    host = CharField(unique=True)
    created_at = BigIntegerField()
    is_registered = peewee.BooleanField(default=False)


# get all es servers
@app.route('/api/v1/elastic-server/all', methods=['GET'])
def getAllServers():
    servers = []
    for server in ElasticServer.select():
        print(server)
        servers.append(model_to_dict(server))
    return json.dumps(servers)


# get an es server by id
@app.route('/api/v1/elastic-server', methods=['GET'])
def getServerById():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No server id field provided. Please specify an id."
    try:
        server = ElasticServer.get(ElasticServer.id == id)
    except:
        return "No elastic server found"
    return json.dumps(model_to_dict(server))


# save an es server
@app.route('/api/v1/elastic-server', methods=['POST'])
def createESServer():
    try:
        server = ElasticServer.create(host=request.json['host'], created_at=getCurrentTimeMillis())
        server.save()
    except peewee.IntegrityError:
        return "Elastic server is already added."
    return json.dumps(model_to_dict(server))


if __name__ == '__main__':
    app.run()

    db.connect()
    db.create_tables([ElasticServer])
