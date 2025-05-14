class ResultParser:
    @staticmethod
    def parse_alerts(alerts):
        parsed_results = {
            'alerts': [],
            'summary': {
                'High': 0,
                'Medium': 0,
                'Low': 0,
                'Informational': 0
            }
        }
        
        for alert in alerts:
            severity = alert.get('risk', 'Informational')
            parsed_results['summary'][severity] += 1
            
            parsed_results['alerts'].append({
                'name': alert.get('name', 'Unknown'),
                'risk': severity,
                'url': alert.get('url', ''),
                'description': alert.get('description', ''),
                'solution': alert.get('solution', ''),
                'reference': alert.get('reference', '')
            })
            
        return parsed_results