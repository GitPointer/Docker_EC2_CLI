from flask import Flask
from flask import render_template, request, redirect
from redis import Redis
import requests
import os

app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/')
@app.route('/index')
def index():
    count = redis.incr('hits')
    return render_template("index.html",hits=count)


@app.route('/process', methods=['POST'])
def process_text():
    count = redis.incr('hits')
    input_text = request.form['input_text']

    output_text = input_text

    if 'to_lower' in request.form:
        TO_LOWER_SERVICE_PORT = os.environ.get('TO_LOWER_SERVICE_PORT', '5003')
        TO_LOWER_SERVICE_NAME = os.environ.get('TO_LOWER_SERVICE_NAME', 'text-to_lower-service')
        TO_LOWER_SERVICE_HOST = 'http://' + TO_LOWER_SERVICE_NAME + ':' + TO_LOWER_SERVICE_PORT
        try:
            response = requests.get(TO_LOWER_SERVICE_HOST + '/api/v0/to_lower', json={'input_text': str(output_text)})
            output_text = response.json()['output_text']
        except requests.exceptions.RequestException as e:
            output_text = str(e)

    if 'to_upper' in request.form:
        TO_UPPER_SERVICE_PORT = os.environ.get('TO_UPPER_SERVICE_PORT', '5002')
        TO_UPPER_SERVICE_NAME = os.environ.get('TO_UPPER_SERVICE_NAME', 'text-to_upper-service')
        TO_UPPER_SERVICE_HOST = 'http://' + TO_UPPER_SERVICE_NAME + ':' + TO_UPPER_SERVICE_PORT
        try:
            response = requests.get(TO_UPPER_SERVICE_HOST + '/api/v0/to_upper', json={'input_text': str(output_text)})
            output_text = response.json()['output_text']
        except requests.exceptions.RequestException as e:
            output_text = str(e)

    if 'revert' in request.form:
        REVERT_SERVICE_PORT = os.environ.get('REVERT_SERVICE_PORT', '5001')
        REVERT_SERVICE_NAME = os.environ.get('REVERT_SERVICE_NAME', 'text-revert-service')
        REVERT_SERVICE_HOST = 'http://' + REVERT_SERVICE_NAME + ':' + REVERT_SERVICE_PORT
        try:
            response = requests.get(REVERT_SERVICE_HOST + '/api/v0/revert', json={'input_text': str(output_text)})
            output_text = response.json()['output_text']
        except requests.exceptions.RequestException as e:
            output_text = str(e)

    return render_template("index.html", input_text=input_text, output_text=output_text,hits=count)


if __name__ == '__main__':
    PORT = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=PORT)