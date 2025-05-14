import json
import re
from datetime import datetime

def parse_results(test_output):
    steps = []
    current_step = 1
    
    # Parse test output
    lines = test_output['stdout'].split('\n')
    for line in lines:
        if line.strip():
            # Basic parsing - can be enhanced based on actual output format
            status = 'passed' if 'PASS' in line.upper() else 'failed'
            steps.append({
                'number': current_step,
                'description': line.strip(),
                'status': status,
                'duration': float(f"{float(re.search(r'(\d+\.\d+)s', line).group(1)):.4f}")
                if re.search(r'(\d+\.\d+)s', line) 
                else 0.0000
                ,
                'timestamp': datetime.now().isoformat()
            })
            current_step += 1
    
    # Calculate summary
    passed = sum(1 for step in steps if step['status'] == 'passed')
    failed = sum(1 for step in steps if step['status'] == 'failed')
    total_duration = sum(step['duration'] for step in steps)
    
    return {
        'total_steps': len(steps),
        'passed_steps': passed,
        'failed_steps': failed,
        'error_steps': len(steps) - passed - failed,
        'duration': round(total_duration, 2),
        'steps': steps,
        'timestamp': datetime.now().isoformat()
    }
import json
import re
from datetime import datetime

def parse_results(test_output):
    steps = []
    current_step = 1
    
    # Parse test output
    lines = test_output['stdout'].split('\n')
    for line in lines:
        if line.strip():
            # Basic parsing - can be enhanced based on actual output format
            status = 'passed' if 'PASS' in line.upper() else 'failed'
            steps.append({
                'number': current_step,
                'description': line.strip(),
                'status': status,
                'duration': float(f"{float(re.search(r'(\d+\.\d+)s', line).group(1)):.4f}")
                if re.search(r'(\d+\.\d+)s', line) 
                else 0.0000
                ,
                'timestamp': datetime.now().isoformat()
            })
            current_step += 1
    
    # Calculate summary
    passed = sum(1 for step in steps if step['status'] == 'passed')
    failed = sum(1 for step in steps if step['status'] == 'failed')
    total_duration = sum(step['duration'] for step in steps)
    
    return {
        'total_steps': len(steps),
        'passed_steps': passed,
        'failed_steps': failed,
        'error_steps': len(steps) - passed - failed,
        'duration': round(total_duration, 2),
        'steps': steps,
        'timestamp': datetime.now().isoformat()
    }
