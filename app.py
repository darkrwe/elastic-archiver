#!/usr/bin/env python3
import json
import flask
import peewee
from flask import request, Response
from peewee import Model, BigIntegerField, CharField
from playhouse.shortcuts import model_to_dict

from util import getCurrentTimeMillis

app = flask.Flask(__name__)
# app.config["DEBUG"] = True
db = peewee.SqliteDatabase('elastic-archiver.db')


class BaseModel(Model):
    class Meta:
        database = db


class ElasticServer(BaseModel):
    id = BigIntegerField(primary_key=True, unique=True)
    host = CharField(unique=True)
    region = CharField(unique=True, default="us-east-1")
    created_at = BigIntegerField()
    is_registered = peewee.BooleanField(default=False)


resp = {
    'data': {},
    'path': '',
    'message': '',
    'errors': [],
    'timestamp': ''
}


# get all es servers
@app.route('/api/v1/elastic-server/all', methods=['GET'])
def getAllServers():
    servers = []
    for server in ElasticServer.select():
        print(server)
        servers.append(model_to_dict(server))
    return generateSuccessResponse(servers)


# get an es server by id
@app.route('/api/v1/elastic-server', methods=['GET'])
def getServerById():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return generateErrorResponse(None, "No server id field provided. Please specify an id.", [], 400)
    try:
        server = ElasticServer.get(ElasticServer.id == id)
    except:
        return generateErrorResponse(None, "No server id field provided. Please specify an id.", [], 400)
    return generateSuccessResponse(model_to_dict(server))


# save an es server
@app.route('/api/v1/elastic-server', methods=['POST'])
def createESServer():
    try:
        server = ElasticServer.create(host=request.json['host'], created_at=getCurrentTimeMillis(),
                                      region=request.json['region'])
        server.save()
    except peewee.IntegrityError:
        return generateErrorResponse(None, "Elastic server is already added", [], 400)
    return generateSuccessResponse(model_to_dict(server))


# register an es server to repo
@app.route('/api/v1/elastic-server/register/<server_id>', methods=['POST'])
def registerESServer(server_id):
    try:
        server = ElasticServer.get(ElasticServer.id == server_id)

        if server.is_registered is True:
            return generateErrorResponse(None, "Server is already registered", [], 400)
        else:
            return generateSuccessResponse(True)

    except Exception:
        return generateErrorResponse(None, "Something went wrong while registering server", [], 500)

    return generateSuccessResponse(True)


def generateSuccessResponse(data):
    resp['data'] = data
    resp['timestamp'] = getCurrentTimeMillis()
    resp['path'] = request.path
    resp['errors'] = []
    resp['message'] = ""
    return Response(json.dumps(resp), status=200, mimetype='application/json')


def generateErrorResponse(data, message, errors, statusCode):
    resp['data'] = data
    resp['timestamp'] = getCurrentTimeMillis()
    resp['path'] = request.path
    resp['errors'] = errors
    resp['message'] = message
    return Response(json.dumps(resp), status=statusCode, mimetype='application/json')


if __name__ == '__main__':
    app.run()

    db.connect()
    db.create_tables([ElasticServer])
