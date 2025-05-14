from flask import Flask, render_template, request, send_from_directory, jsonify
from services.zap_scanner import SecurityScanner
from services.result_parser import ResultParser
from services.report_generator import ReportGenerator
from config import Config
import os

app = Flask(__name__)
Config.init_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target_url = request.form.get('url')
    if not target_url:
        return jsonify({'error': 'URL is required'}), 400
        
    try:
        # Initialize scanner and perform scan
        scanner = SecurityScanner()
        alerts = scanner.scan_url(target_url)
        
        # Parse results
        parser = ResultParser()
        parsed_results = parser.parse_alerts(alerts)
        
        # Generate PDF report
        report_gen = ReportGenerator(parsed_results)
        pdf_filename = report_gen.generate_pdf(target_url)
        
        return render_template('dashboard.html',
                             results=parsed_results,
                             target_url=target_url,
                             pdf_filename=pdf_filename)
                             
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/scan-status')
def scan_status():
    # This is a simplified status - in a real app, you'd track actual progress
    stages = [
        "Initializing ZAP Scanner",
        "Spider Crawling",
        "Passive Scanning",
        "Active Scanning",
        "Analyzing Results",
        "Generating Report"
    ]
    current_stage = request.args.get('stage', 0, type=int)
    if current_stage >= len(stages):
        return jsonify({'complete': True})
    return jsonify({
        'stage': stages[current_stage],
        'progress': (current_stage + 1) * (100 // len(stages)),
        'complete': False
    })

@app.route('/download/<filename>')
def download_report(filename):
    return send_from_directory(Config.RESULTS_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True,port=5003)