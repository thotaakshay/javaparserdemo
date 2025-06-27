from flask import Flask, request, jsonify
from extract_method import extract_method
from junit_test_generator import generate_junit_test
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    java_file = None
    # handle raw code
    if data.get('code'):
        java_file = 'TempInput.java'
        with open(java_file, 'w') as f:
            f.write(data['code'])
    elif data.get('file_path'):
        java_file = data['file_path']
    else:
        return jsonify({'error': 'Provide code or file_path'}), 400

    method_code = extract_method(java_file)
    if method_code is None:
        return jsonify({'error': 'Failed to extract method'}), 500

    junit_test = generate_junit_test(method_code)
    return jsonify({'junit_test': junit_test})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
