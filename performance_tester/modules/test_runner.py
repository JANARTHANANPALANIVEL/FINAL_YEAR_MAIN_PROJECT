import os
from .lighthouse_runner import LighthouseRunner
from .result_parser import ResultParser
from .report_generator import ReportGenerator

class TestRunner:
    def __init__(self, url, test_id, results_dir):
        self.url = url
        self.test_id = test_id
        self.results_dir = results_dir
        
    def run(self):
        """
        Coordinates the entire test process:
        1. Runs Lighthouse test
        2. Parses results
        3. Generates report
        """
        try:
            # Create a specific directory for this test
            test_dir = os.path.join(self.results_dir, self.test_id)
            os.makedirs(test_dir, exist_ok=True)
            
            # Run Lighthouse test
            lighthouse = LighthouseRunner(self.url, test_dir)
            result_file = lighthouse.run()
            
            # Rename the result file to include test_id
            final_result_file = os.path.join(self.results_dir, f'{self.test_id}_results.json')
            os.rename(result_file, final_result_file)
            
            # Parse results
            parser = ResultParser(final_result_file)
            metrics = parser.get_metrics()
            
            # Generate report
            report_gen = ReportGenerator(metrics, self.results_dir)
            report_file = report_gen.generate_pdf(self.test_id)
            
            # Clean up test directory if empty
            try:
                os.rmdir(test_dir)
            except:
                pass
                
            return {
                'success': True,
                'metrics': metrics,
                'report_file': report_file
            }
            
        except Exception as e:
            return {
                'error': str(e)
            }
