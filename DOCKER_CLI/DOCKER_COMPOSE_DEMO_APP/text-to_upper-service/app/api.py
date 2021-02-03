import os

from flask import Flask
from flask import request, jsonify

import sys

app = Flask(__name__)


@app.route('/api/v0/to_upper', methods=['GET'])
def text_to_upper():
    try:
        input_text = request.get_json()['input_text']
    except:
        e = sys.exc_info()[0]
        return jsonify({'error': str(e)})

    output_text = input_text.upper()
    return jsonify({"output_text": str(output_text)})


@app.route('/')
def index():
    return 'text-upper-service'


if __name__ == '__main__':
    PORT = os.environ.get('PORT', 5002)
    print(PORT)
    app.run(debug=True, host='0.0.0.0', port=PORT)
