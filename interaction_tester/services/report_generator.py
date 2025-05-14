from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from datetime import datetime

def generate_pdf_report(results, test_id):
    pdf_path = os.path.join('results', f'report_{test_id}.pdf')
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    elements.append(Paragraph('Test Execution Report', styles['Title']))
    elements.append(Spacer(1, 20))
    
    # Summary
    summary_data = [
        ['Total Steps', str(results['total_steps'])],
        ['Passed Steps', str(results['passed_steps'])],
        ['Failed Steps', str(results['failed_steps'])],
        ['Error Steps', str(results['error_steps'])],
        ['Total Duration', f"{results['duration']}s"]
    ]
    
    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    # Detailed Steps
    elements.append(Paragraph('Test Steps', styles['Heading1']))
    elements.append(Spacer(1, 10))
    
    steps_data = [['Step', 'Description', 'Status', 'Duration']]
    for step in results['steps']:
        steps_data.append([
            str(step['number']),
            step['description'],
            step['status'],
            f"{step['duration']}s"
        ])
    
    steps_table = Table(steps_data)
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(steps_table)
    
    doc.build(elements)
    return pdf_path