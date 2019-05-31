import json

from flask import Response, request

from util import getCurrentTimeMillis

resp = {
    'data': {},
    'path': '',
    'message': '',
    'errors': [],
    'timestamp': ''
}

HttpStatusCodes = {
    'OK': 200,
    'BAD_REQUEST': 400,
    'INTERNAL_SERVER_ERROR': 500
}


def generateSuccessResponse(data):
    resp['data'] = data
    resp['timestamp'] = getCurrentTimeMillis()
    resp['path'] = request.path
    resp['errors'] = []
    resp['message'] = ""
    return Response(json.dumps(resp), status=HttpStatusCodes['OK'], mimetype='application/json')


def generateErrorResponse(data, message, errors, statusCode):
    resp['data'] = data
    resp['timestamp'] = getCurrentTimeMillis()
    resp['path'] = request.path
    resp['errors'] = errors
    resp['message'] = message
    return Response(json.dumps(resp), status=statusCode, mimetype='application/json')
