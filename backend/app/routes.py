from flask import jsonify, request
from app import app
from algorithm.model import ModelName

model = ModelName()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json

    query = data['query']

    res = model.analyze(query)


    return jsonify({'status': 0, 'result': res})
