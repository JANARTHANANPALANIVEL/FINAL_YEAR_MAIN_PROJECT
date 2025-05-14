import subprocess
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LighthouseRunner:
    def __init__(self, url, output_dir):
        self.url = url
        self.output_dir = output_dir
        self.lighthouse_path = os.getenv('LIGHTHOUSE_PATH', 'lighthouse')
        self.chrome_path = os.getenv('CHROME_PATH', '/usr/bin/google-chrome')
        
    def run(self):
        """
        Runs Lighthouse test using Node.js lighthouse CLI
        Returns the path to the JSON results file
        """
        try:
            output_file = os.path.join(self.output_dir, 'lighthouse_results.json')
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Run lighthouse using Node.js
            command = [
                self.lighthouse_path,
                self.url,
                '--output=json',
                '--output-path=' + output_file,
                '--chrome-path=' + self.chrome_path,
                '--chrome-flags="--headless --no-sandbox"'
            ]
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8'
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Lighthouse test failed: {stderr}")
                
            # Verify the file was created
            if not os.path.exists(output_file):
                raise Exception("Lighthouse did not generate the results file")
                
            return output_file
            
        except Exception as e:
            raise Exception(f"Error running Lighthouse: {str(e)}")
