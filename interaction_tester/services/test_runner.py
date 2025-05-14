import subprocess
import sys
import os

def run_test(test_file_path):
    try:
        result = subprocess.run(
            [sys.executable, test_file_path],
            capture_output=True,
            text=True,
            env=os.environ.copy()
        )
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': str(e),
            'returncode': 1
        }