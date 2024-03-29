from flask import Flask, jsonify, request
import json
from rich.console import Console
import src.tools

console = Console()
app = Flask(__name__)


@app.route('/update', methods=['POST'])
async def update():
    data = request.get_json()
    if data:
        return jsonify({'error': 'No input data needed'}), 400
    elapsed_time = await src.tools.update()
    return jsonify({'result': elapsed_time}), 200


@app.route('/api', methods=['POST'])
async def check_json():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    message = data['message']
    console.log(message)
    result = await src.tools.scan_db("./words.db", data['message'])

    return jsonify({'result': result}), 200


if __name__ == '__main__':
    app.run(debug=True, port=8001)
