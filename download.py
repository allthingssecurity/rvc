from flask import Flask, request, send_from_directory, jsonify, abort
import os

app = Flask(__name__)

# Directory where the weights are stored
WEIGHTS_DIR = 'weights'

@app.route('/get_weights', methods=['POST'])
def get_weights():
    # Example: expecting a JSON payload with the model name to select the correct weights file
    if not request.json or 'model_name' not in request.json:
        return jsonify({'error': 'Request must include model_name'}), 400
    
    model_name = request.json['model_name']
    file_path = os.path.join(WEIGHTS_DIR, f"{model_name}.pth")

    # Check if the file exists
    if not os.path.isfile(file_path):
        return abort(404, description="Weights file not found.")

    # Send the file back to the client
    return send_from_directory(directory=WEIGHTS_DIR, path=f"{model_name}.pth", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
