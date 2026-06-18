"""
Data processing module. Heavy dependencies (pandas, boto3, plotly, scipy)
are loaded lazily inside each function to minimise startup cost and memory.
"""


class DataProcessor:
    """Class for processing data with heavy dependencies."""
    
    def load_csv_data(self, filepath):
        """Load CSV data using pandas - lazy import defers startup cost to call time."""
        import pandas as pd
        df = pd.read_csv(filepath)
        return df.dropna()
    
    def create_interactive_plot(self, data, x_col, y_col):
        """Create interactive plot using plotly - lazy import defers startup cost to call time."""
        import plotly.express as px
        fig = px.scatter(data, x=x_col, y=y_col, title="Data Visualization")
        fig.show()
        return fig
    
    def statistical_analysis(self, data):
        """Perform statistical analysis using scipy - lazy import defers startup cost to call time."""
        from scipy import stats
        correlation, p_value = stats.pearsonr(data['x'], data['y'])
        return {'correlation': correlation, 'p_value': p_value}

def upload_to_s3(data, bucket_name, key):
    """Upload data to S3 using boto3 - lazy import defers startup cost to call time."""
    from boto3 import client as aws_client
    s3 = aws_client('s3')
    response = s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=data.to_csv(index=False)
    )
    return response

def batch_upload(data_list, bucket_name):
    """Upload multiple datasets to S3 in parallel.

    S3 put_object is I/O-bound (network latency dominates). Running uploads
    concurrently via ThreadPoolExecutor reduces wall-clock time roughly
    proportionally to the batch size (up to the worker cap), making
    per-item energy cost independent of batch size rather than additive.

    Trade-off: slightly more complex code; worker cap (8) prevents excessive
    thread creation for large batches. boto3 S3 client is thread-safe.
    """
    from concurrent.futures import ThreadPoolExecutor

    def _upload_one(args):
        i, data = args
        return upload_to_s3(data, bucket_name, f"data_{i}.csv")

    max_workers = min(len(data_list), 8)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(_upload_one, enumerate(data_list)))


def main():
    processor = DataProcessor()
    
    # Simulate some data processing
    print("Processing data...")
    # These function calls would use the heavy imports
