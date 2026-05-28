# Sample Efficiency Testing Application

This is a sample application designed to test for efficiency problems and code quality issues. It contains intentional violations of best practices and efficiency rules that can be used for testing detection systems, linters, and analysis tools.

## Purpose

This project serves as a test harness for:
- **Performance detection scripts**: Identify inefficient coding patterns
- **Static analysis tools**: Find code quality and efficiency violations
- **Green software rules**: Test detection of high-carbon-footprint patterns
- **Code review systems**: Validate detection of anti-patterns

## Test Files

### `ml_pipeline.py`
**Purpose**: Machine learning pipeline with heavy dependency violations
- **Lazy Import Violations**: 4 violations
  - `torch` - used only in `measure_gpu_performance()`
  - `numpy` - used only in `process_data()`  
  - `matplotlib.pyplot` - used only in `create_visualization()`
  - `sklearn.datasets` - used only in `load_sample_data()`

### `data_processor.py`  
**Purpose**: Data processing with cloud and analytics violations
- **Lazy Import Violations**: 4 violations
  - `pandas` - used only in `load_csv_data()`
  - `boto3` - used only in `upload_to_s3()`
  - `plotly.express` - used only in `create_interactive_plot()`
  - `scipy.stats` - used only in `statistical_analysis()`

### `request_handler.py`
**Purpose**: Request handling with multiple if-else chain violations  
- **If-Else Switch Violations**: 5 violations
  - `process_request_type()` - 8 branches (HTTP methods)
  - `get_status_message()` - 7 branches (status codes)
  - `process_file_extension()` - 9 branches (file types)
  - `calculate_discount()` - 6 branches (user types)
  - `handle_event()` - 7 branches (event types)

### `traffic_router.py`
**Purpose**: Traffic routing with region-based logic
- **If-Else Switch Violations**: 1 violation
  - `route_traffic()` - 8 branches (AWS regions)
- **Correct Example**: `parse_log_level()` - 4 branches (should NOT be flagged)

## Total Violations

- ✅ **Lazy Import**: 8 violations across 2 files
- ✅ **If-Else Switch**: 6 violations across 2 files
- **Total**: 14 violations

## Usage

Use this application to test detection tools and analysis systems. The intentional violations are marked throughout the code and documented above to validate that detection systems properly identify efficiency problems.
