#!/usr/bin/env python
'''Provide mock data for Policy Search that returns JSON'''

from flask import Flask, Response, json, jsonify, request
app = Flask(__name__)

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
        return jsonify({'result': request.args.get('result', 'No POST or GET variables sent')})


if __name__ == '__main__':
    app.run()
