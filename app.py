from flask import Flask, request, jsonify, send_file
from extract_method import extract_method
from junit_test_generator import generate_junit_test
import os
import io
import zipfile

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


@app.route('/generate-tests', methods=['POST'])
def generate_tests():
    """Generate tests for multiple Java source files."""
    data = request.get_json()
    if not data or 'files' not in data:
        return jsonify({'error': 'No files provided'}), 400

    files = data['files']
    if not isinstance(files, list):
        return jsonify({'error': 'files must be a list'}), 400

    # Map of output filename to test content
    test_files = {}
    for file in files:
        name = file.get('name')
        content = file.get('content')
        if not name or content is None:
            continue
        junit = generate_junit_test(content)
        test_name = name.rsplit('.', 1)[0] + 'Test.java'
        test_files[test_name] = junit

    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w') as zf:
        for fname, code in test_files.items():
            zf.writestr(fname, code)
    mem_zip.seek(0)
    return send_file(
        mem_zip,
        mimetype='application/zip',
        as_attachment=True,
        download_name='junit-tests.zip'
    )

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
