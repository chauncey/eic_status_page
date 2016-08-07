#!/usr/bin/env python
'''Provide mock data for Status Check that returns JSON'''

import os
import ssl
import urllib.request
from urllib.error import HTTPError, URLError
from flask import Flask, Response, json, jsonify, request
app = Flask(__name__)
app.debug = os.environ.get('DEBUG')

mock_data = [
    {
        "agents": "down",
        "insureds": "up"
    }
]

context = ssl._create_unverified_context()

def check_agents():
    url = 'https://{}'.format(os.environ.get('AGENTS_URL'))
    try:
        urllib.request.urlopen(url, context=context)
        return {'status': 'up'}
    except HTTPError as e:
        if '401' in str(e):
            return {'status': 'up'}
        return {
            'status': 'unknown',
            'error': 'Error {}'.format(e)
        }

    except URLError as e:
        return {
            'status': 'down',
            'error': 'Error {}'.format(e)
        }


def jsonp(data, callback="function"):
    '''Provide a JSONP response with callback'''
    return Response(
        "%s(%s);" %(callback, json.dumps(data)),
        mimetype="text/javascript"
    )


@app.route('/')
def hello_world():
    '''Obligatory Hello, World!'''
    return 'Hello, World!'


@app.route('/echo', methods=['GET', 'POST'])
def echo():
    '''Echo request variables for testing'''
    if request.method == 'POST':
        jsonbody = json.load(request.stream)
        return jsonify({
            'result': repr(jsonbody)
        })
    elif request.method == 'GET':
        return jsonify({
            'result': request.args
        })
    else:
        return jsonify({
            'result': request.args.get(
                'result', 'No POST or GET variables sent'
            )
        })


@app.route('/eic-status/api/v1.0', methods=['GET'])
@app.route('/eic-status/api/v1.0/<area>', methods=['GET'])
def get_status(area='all'):
    '''Return status of an area or all areas'''
    callback = request.args.get('callback')
    if area in ['all', 'agents']:
        resp = {'agents': check_agents()}
    if callback:
        return jsonp(resp, callback)
    else:
        return jsonp(mock_data)


if __name__ == '__main__':
    app.run()
