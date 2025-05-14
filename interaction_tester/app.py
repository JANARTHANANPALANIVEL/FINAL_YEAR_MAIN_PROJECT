from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import uuid
from services.test_generator import generate_test_case
from services.test_runner import run_test
from services.result_parser import parse_results
from services.report_generator import generate_pdf_report

app = Flask(__name__)

RESULTS_DIR = 'results'
TEST_FILE = 'test_file/generated_test.py'

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs('test_file', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-testcase', methods=['POST'])
def generate_testcase():
    data = request.json
    test_id = str(uuid.uuid4())
    test_case = generate_test_case(
        data['url'],
        data['websiteType'],
        data.get('customPrompt', '')
    )
    
    # Save the generated test case with UUID
    test_file_path = f'test_file/test_{test_id}.py'
    with open(test_file_path, 'w') as f:
        f.write(test_case)
    
    return jsonify({'testCase': test_case, 'testId': test_id})

@app.route('/update-testcase', methods=['POST'])
def update_testcase():
    data = request.json
    test_id = data.get('testId')
    test_file_path = f'test_file/test_{test_id}.py'
    
    with open(test_file_path, 'w') as f:
        f.write(data['code'])
    return jsonify({'status': 'success'})

@app.route('/execute-test', methods=['POST'])
def execute_test():
    data = request.json
    test_id = data.get('testId')
    test_file_path = f'test_file/test_{test_id}.py'
    
    test_output = run_test(test_file_path)
    results = parse_results(test_output)
    
    # Save results with UUID
    results_file = f'results/results_{test_id}.json'
    with open(results_file, 'w') as f:
        json.dump(results, f)
    
    # Generate PDF automatically
    pdf_path = generate_pdf_report(results, test_id)
    
    return jsonify({
        'status': 'success',
        'testId': test_id,
        'pdfPath': pdf_path
    })

@app.route('/dashboard/<test_id>')
def dashboard(test_id):
    results_file = f'results/results_{test_id}.json'
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    return render_template('dashboard.html',
        test_id=test_id,
        total_steps=results['total_steps'],
        passed_steps=results['passed_steps'],
        failed_steps=results['failed_steps'],
        error_steps=results['error_steps'],
        duration=results['duration'],
        test_steps=results['steps'],
        step_numbers=[step['number'] for step in results['steps']],
        step_durations=[step['duration'] for step in results['steps']]
    )

@app.route('/download-report/<test_id>')
def download_report(test_id):
    pdf_path = f'results/report_{test_id}.pdf'
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)