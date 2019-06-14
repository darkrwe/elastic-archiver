#!/usr/bin/env python3
import flask
import peewee
from flask import request
from peewee import Model, BigIntegerField, CharField
from playhouse.shortcuts import model_to_dict
from response_generator import generateSuccessResponse, generateErrorResponse, HttpStatusCodes
from util import getCurrentTimeMillis
import requests
from es_service import registerServer, getSnapshotRepositories

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
        return generateErrorResponse(None, "No server id field provided. Please specify an id.", [],
                                     HttpStatusCodes['BAD_REQUEST'])
    try:
        server = ElasticServer.get(ElasticServer.id == id)
    except:
        return generateErrorResponse(None, "No server id field provided. Please specify an id.", [],
                                     HttpStatusCodes['BAD_REQUEST'])
    return generateSuccessResponse(model_to_dict(server))


# save an es server
@app.route('/api/v1/elastic-server', methods=['POST'])
def createESServer():
    try:
        try:
            server = ElasticServer.create(host=request.json['host'], created_at=getCurrentTimeMillis(),
                                          region=request.json['region'])
            server.save()
        except peewee.IntegrityError:
            return generateErrorResponse(None, "Elastic server is already added", [], HttpStatusCodes['BAD_REQUEST'])
    except Exception:
        return generateErrorResponse(None, "Something went wrong while saving server", [],
                                     HttpStatusCodes['INTERNAL_SERVER_ERROR'])
    return generateSuccessResponse(model_to_dict(server))


# register an es server to repo
@app.route('/api/v1/elastic-server/register/<server_id>', methods=['POST'])
def registerESServer(server_id):
    try:
        server = ElasticServer.get(ElasticServer.id == server_id)

        if server.is_registered is True:
            return generateErrorResponse(None, "Server is already registered", [], HttpStatusCodes['BAD_REQUEST'])
        else:
            result = registerServer(server.host,
                                    server.region,
                                    request.json['repository_name'],
                                    request.json['bucket'],
                                    request.json['role_name'],
                                    request.json['account_id'], )
            if result is None:
                return generateErrorResponse(None, "Something went wrong while registering server", [],
                                             HttpStatusCodes['INTERNAL_SERVER_ERROR'])
            else:
                server.is_registered = True
                server.save()
                return generateSuccessResponse(result)

    except Exception:
        return generateErrorResponse(None, "Something went wrong while registering server", [],
                                     HttpStatusCodes['INTERNAL_SERVER_ERROR'])

    return generateSuccessResponse(True)


# Get snapshot repositories
@app.route('/api/v1/elastic-server/snapshot-repository/<server_id>', methods=['GET'])
def getSSRepositories(server_id):
    try:
        server = ElasticServer.get(ElasticServer.id == server_id)

        if server.is_registered is False:
            return generateErrorResponse(None, "Server is not registered", [], HttpStatusCodes['BAD_REQUEST'])
        else:
            result = getSnapshotRepositories(server.host)
            if result is None:
                return generateErrorResponse(None, "Something went wrong while getting snapshot repositories", [],
                                             HttpStatusCodes['INTERNAL_SERVER_ERROR'])
            else:
                return generateSuccessResponse(result)

    except Exception:
        return generateErrorResponse(None, "Something went wrong while getting snapshot repositories", [],
                                     HttpStatusCodes['INTERNAL_SERVER_ERROR'])

    return generateSuccessResponse(True)


if __name__ == '__main__':
    app.run()

    db.connect()
    db.create_tables([ElasticServer])
