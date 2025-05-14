from flask import Flask, render_template, request, send_file, jsonify
import os
from datetime import datetime
from modules.lighthouse_runner import LighthouseRunner
from modules.result_parser import ResultParser
from modules.report_generator import ReportGenerator
from modules.test_runner import TestRunner
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get configuration from environment variables
RESULTS_DIR = os.getenv('RESULTS_DIR', 'results')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# Ensure results directory exists with absolute path
RESULTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), RESULTS_DIR))
os.makedirs(RESULTS_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-test', methods=['POST'])
def run_test():
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Create unique test ID using timestamp
        test_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Initialize test runner
        test_runner = TestRunner(url, test_id, RESULTS_DIR)
        
        # Run the test and get results
        result = test_runner.run()
        
        if result.get('error'):
            return jsonify({'error': result['error']}), 400
            
        return jsonify({
            'success': True,
            'test_id': test_id,
            'metrics': result['metrics'],
            'report_url': f'/download-report/{test_id}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard/<test_id>')
def dashboard(test_id):
    try:
        # Load test results
        result_file = os.path.join(RESULTS_DIR, f'{test_id}_results.json')
        parser = ResultParser(result_file)
        metrics = parser.get_metrics()
        
        return render_template('dashboard.html', 
                             metrics=metrics,
                             test_id=test_id)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/download-report/<test_id>')
def download_report(test_id):
    try:
        report_file = os.path.join(RESULTS_DIR, f'{test_id}_report.pdf')
        return send_file(report_file,
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name=f'performance_report_{test_id}.pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host=HOST, port=5002, debug=DEBUG)
