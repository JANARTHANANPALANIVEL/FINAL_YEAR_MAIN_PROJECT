import time
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
from config import Config

class ReportGenerator:
    def __init__(self, scan_results):
        self.results = scan_results
        self.styles = getSampleStyleSheet()
        
    def generate_pdf(self, target_url):
        filename = f"scan_report_{int(time.time())}.pdf"
        filepath = os.path.join(Config.RESULTS_FOLDER, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        story.append(Paragraph(f"Security Scan Report for {target_url}", title_style))
        story.append(Spacer(1, 12))
        
        # Summary
        story.append(Paragraph("Summary", self.styles['Heading2']))
        summary_data = [['Severity', 'Count']]
        for severity, count in self.results['summary'].items():
            summary_data.append([severity, str(count)])
            
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Detailed Findings
        story.append(Paragraph("Detailed Findings", self.styles['Heading2']))
        for alert in self.results['alerts']:
            story.append(Paragraph(f"Finding: {alert['name']}", self.styles['Heading3']))
            story.append(Paragraph(f"Risk Level: {alert['risk']}", self.styles['Normal']))
            story.append(Paragraph(f"URL: {alert['url']}", self.styles['Normal']))
            story.append(Paragraph(f"Description: {alert['description']}", self.styles['Normal']))
            story.append(Paragraph(f"Solution: {alert['solution']}", self.styles['Normal']))
            story.append(Spacer(1, 12))
            
        doc.build(story)
        return filename