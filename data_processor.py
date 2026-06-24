"""
Data processing module. Heavy dependencies (pandas, boto3, plotly, scipy)
are loaded lazily inside each function to minimise startup cost and memory.
"""
import functools

from functools import lru_cache


class DataProcessor:
    """Class for processing data with heavy dependencies."""

    @staticmethod
    @lru_cache(maxsize=128)
    def load_csv_data(filepath):
        """Load CSV data using pandas - lazy import defers startup cost to call time.

        Results are cached by filepath so repeated calls for the same file avoid
        disk I/O and pandas parse overhead entirely.

        Note: the cached DataFrame is shared across all callers. Mutating the
        returned DataFrame will affect all subsequent callers receiving the same
        cached object. Copy with df.copy() before in-place modifications.
        """
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

@functools.lru_cache(maxsize=1)
def _get_s3_client():
    """Return a module-level cached boto3 S3 client.

    lru_cache ensures the client is created exactly once per process, avoiding
    repeated credential resolution and HTTP-session setup on every upload call.
    The boto3 S3 client is thread-safe for concurrent put_object calls.
    Trade-off: cached client is not invalidated if credentials rotate mid-process.
    """
    from boto3 import client as aws_client
    return aws_client('s3')

def upload_to_s3(data, bucket_name, key):
    """Upload data to S3 using boto3 - lazy import defers startup cost to call time."""
    s3 = _get_s3_client()
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
