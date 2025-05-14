import json

class ResultParser:
    def __init__(self, result_file):
        self.result_file = result_file
        
    def get_metrics(self):
        """
        Parses Lighthouse JSON results and extracts key metrics
        """
        try:
            with open(self.result_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            audits = data['audits']
            
            metrics = {
                'first-contentful-paint': {
                    'score': audits['first-contentful-paint']['score'],
                    'value': audits['first-contentful-paint']['numericValue']
                },
                'speed-index': {
                    'score': audits['speed-index']['score'],
                    'value': audits['speed-index']['numericValue']
                },
                'largest-contentful-paint': {
                    'score': audits['largest-contentful-paint']['score'],
                    'value': audits['largest-contentful-paint']['numericValue']
                },
                'total-blocking-time': {
                    'score': audits['total-blocking-time']['score'],
                    'value': audits['total-blocking-time']['numericValue']
                },
                'cumulative-layout-shift': {
                    'score': audits['cumulative-layout-shift']['score'],
                    'value': audits['cumulative-layout-shift']['numericValue']
                }
            }
            
            return metrics
            
        except Exception as e:
            raise Exception(f"Error parsing results: {str(e)}")
