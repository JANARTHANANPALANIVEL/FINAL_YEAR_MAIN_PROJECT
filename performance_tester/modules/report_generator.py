from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
import os

class ReportGenerator:
    def __init__(self, metrics, output_dir):
        self.metrics = metrics
        self.output_dir = output_dir
        
    def generate_charts(self):
        """
        Generates multiple performance metric charts using matplotlib
        """
        charts = {}
        
        # 1. Bar chart for performance scores
        plt.figure(figsize=(10, 6))
        scores = [m['score'] for m in self.metrics.values()]
        labels = [label.replace('-', ' ').title() for label in self.metrics.keys()]
        
        plt.bar(labels, scores, color='skyblue')
        plt.xticks(rotation=45)
        plt.title('Performance Metrics Scores')
        plt.ylim(0, 1)  # Scores are between 0 and 1
        plt.tight_layout()
        
        score_chart = os.path.join(self.output_dir, 'performance_scores.png')
        plt.savefig(score_chart)
        plt.close()
        charts['scores'] = score_chart

        # 2. Radar chart for comprehensive view
        plt.figure(figsize=(8, 8))
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
        
        # Close the plot by appending the first value
        values = np.concatenate((scores, [scores[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        labels_plot = np.concatenate((labels, [labels[0]]))
        
        ax = plt.subplot(111, projection='polar')
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels_plot[:-1])
        plt.title('Performance Metrics Overview')
        
        radar_chart = os.path.join(self.output_dir, 'performance_radar.png')
        plt.savefig(radar_chart)
        plt.close()
        charts['radar'] = radar_chart

        # 3. Timeline chart for timing metrics
        plt.figure(figsize=(10, 6))
        values = [m['value'] for m in self.metrics.values()]
        
        plt.plot(labels, values, marker='o')
        plt.xticks(rotation=45)
        plt.title('Performance Timing Metrics')
        plt.ylabel('Time (ms)')
        plt.grid(True)
        plt.tight_layout()
        
        timeline_chart = os.path.join(self.output_dir, 'performance_timeline.png')
        plt.savefig(timeline_chart)
        plt.close()
        charts['timeline'] = timeline_chart
        
        return charts
        
    def generate_pdf(self, test_id):
        """
        Generates PDF report with performance metrics, tables, and charts
        """
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Performance Test Report', ln=True, align='C')
        pdf.ln(10)
        
        # Summary Table
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Performance Metrics Summary', ln=True)
        pdf.ln(5)
        
        # Table headers
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(60, 10, 'Metric', 1)
        pdf.cell(40, 10, 'Score', 1)
        pdf.cell(40, 10, 'Value (ms)', 1)
        pdf.ln()
        
        # Table content
        pdf.set_font('Arial', '', 12)
        for metric, data in self.metrics.items():
            metric_name = metric.replace('-', ' ').title()
            pdf.cell(60, 10, metric_name, 1)
            pdf.cell(40, 10, f"{data['score']:.2f}", 1)
            pdf.cell(40, 10, f"{data['value']:.2f}", 1)
            pdf.ln()
        
        pdf.ln(10)
        
        # Analysis section
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Performance Analysis', ln=True)
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        for metric, data in self.metrics.items():
            metric_name = metric.replace('-', ' ').title()
            score = data['score']
            
            # Add performance assessment
            pdf.cell(0, 10, f"{metric_name}:", ln=True)
            if score >= 0.9:
                assessment = "Excellent"
            elif score >= 0.7:
                assessment = "Good"
            elif score >= 0.5:
                assessment = "Needs Improvement"
            else:
                assessment = "Poor"
                
            pdf.cell(0, 10, f"Score: {score:.2f} - {assessment}", ln=True)
            pdf.ln(5)
        
        # Add charts
        charts = self.generate_charts()
        
        # Performance Scores Chart
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Performance Scores Visualization', ln=True)
        pdf.image(charts['scores'], x=10, y=None, w=190)
        
        # Radar Chart
        pdf.add_page()
        pdf.cell(0, 10, 'Performance Metrics Overview', ln=True)
        pdf.image(charts['radar'], x=10, y=None, w=190)
        
        # Timeline Chart
        pdf.add_page()
        pdf.cell(0, 10, 'Performance Timing Analysis', ln=True)
        pdf.image(charts['timeline'], x=10, y=None, w=190)
        
        # Clean up chart files
        for chart in charts.values():
            os.remove(chart)
        
        # Save PDF
        output_path = os.path.join(self.output_dir, f'{test_id}_report.pdf')
        pdf.output(output_path)
        
        return output_path
