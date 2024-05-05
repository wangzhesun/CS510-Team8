from flask import jsonify, request
from app import app

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json

    query = data['query']


    return jsonify({'message': 'success'})
