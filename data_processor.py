"""
Test file with intentional lazy import violations for data processing.
"""

# Violation 3: pandas imported at top level but only used inside functions
import pandas as pd
from boto3 import client as aws_client

# Additional heavy imports that are only used in functions
import plotly.express as px
import scipy.stats as stats

class DataProcessor:
    """Class for processing data with heavy dependencies."""
    
    def load_csv_data(self, filepath):
        """Load CSV data using pandas - should be lazy imported."""
        df = pd.read_csv(filepath)
        return df.dropna()
    
    def create_interactive_plot(self, data, x_col, y_col):
        """Create interactive plot using plotly - should be lazy imported."""
        fig = px.scatter(data, x=x_col, y=y_col, title="Data Visualization")
        fig.show()
        return fig
    
    def statistical_analysis(self, data):
        """Perform statistical analysis using scipy - should be lazy imported."""
        correlation, p_value = stats.pearsonr(data['x'], data['y'])
        return {'correlation': correlation, 'p_value': p_value}

def upload_to_s3(data, bucket_name, key):
    """Upload data to S3 using boto3 - should be lazy imported."""
    s3 = aws_client('s3')
    response = s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=data.to_csv(index=False)
    )
    return response

def main():
    processor = DataProcessor()
    
    # Simulate some data processing
    print("Processing data...")
    # These function calls would use the heavy imports
