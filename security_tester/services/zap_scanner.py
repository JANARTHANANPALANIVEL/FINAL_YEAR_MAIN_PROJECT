from zapv2 import ZAPv2
from config import Config
import time

class SecurityScanner:
    def __init__(self):
        self.zap = ZAPv2(apikey=Config.ZAP_API_KEY, 
                        proxies={'http': f'http://localhost:{Config.ZAP_PORT}', 
                                'https': f'http://localhost:{Config.ZAP_PORT}'})

    def scan_url(self, target_url):
        try:
            # Access the target URL
            self.zap.urlopen(target_url)
            # Wait for passive scanning to complete
            time.sleep(2)
            
            # Start active scanning
            scan_id = self.zap.ascan.scan(target_url)
            
            # Wait for the active scan to complete
            while int(self.zap.ascan.status(scan_id)) < 100:
                time.sleep(5)
            
            # Get all alerts
            alerts = self.zap.core.alerts()
            return alerts
            
        except Exception as e:
            raise Exception(f"Scanning failed: {str(e)}")

    def get_alerts_summary(self):
        summary = {
            'High': 0,
            'Medium': 0,
            'Low': 0,
            'Informational': 0
        }
        
        alerts = self.zap.core.alerts()
        for alert in alerts:
            risk = alert.get('risk')
            if risk in summary:
                summary[risk] += 1
                
        return summary