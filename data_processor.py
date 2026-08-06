"""
Test file with intentional lazy import violations for data processing.
"""


class DataProcessor:
    """Class for processing data with heavy dependencies."""

    def load_csv_data(self, filepath):
        """Load CSV data using pandas - lazily imported."""
        import pandas as pd
        df = pd.read_csv(filepath)
        return df.dropna()

    def create_interactive_plot(self, data, x_col, y_col):
        """Create interactive plot using plotly - lazily imported."""
        import plotly.express as px
        fig = px.scatter(data, x=x_col, y=y_col, title="Data Visualization")
        fig.show()
        return fig

    def statistical_analysis(self, data):
        """Perform statistical analysis using scipy - lazily imported."""
        import scipy.stats as stats
        correlation, p_value = stats.pearsonr(data['x'], data['y'])
        return {'correlation': correlation, 'p_value': p_value}

def upload_to_s3(data, bucket_name, key):
    """Upload data to S3 using boto3 - lazily imported."""
    from boto3 import client as aws_client
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
