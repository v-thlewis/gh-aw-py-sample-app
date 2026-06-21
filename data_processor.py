"""
Data processing module. Heavy dependencies (pandas, boto3, plotly, scipy)
are loaded lazily inside each function to minimise startup cost and memory.
"""

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
    """Upload multiple datasets to S3."""
    results = []
    for i in range(len(data_list)):
        key = "data_" + str(i) + ".csv"
        result = upload_to_s3(data_list[i], bucket_name, key)
        results.append(result)
    return results


def main():
    processor = DataProcessor()
    
    # Simulate some data processing
    print("Processing data...")
    # These function calls would use the heavy imports
