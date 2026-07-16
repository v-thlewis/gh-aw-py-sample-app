"""
ML pipeline module. Heavy dependencies (torch, numpy, matplotlib, sklearn)
are loaded lazily inside each function to minimise startup cost and memory.
"""
import functools


def measure_gpu_performance():
    """Function that uses torch - lazy import defers startup cost to call time."""
    import torch
    import numpy as np
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tensor = torch.randn(1000, 1000, device=device)
    result = torch.matmul(tensor, tensor.t())
    return result.cpu().numpy()

def create_visualization(data):
    """Function that uses matplotlib - lazy import defers startup cost to call time.

    plt.close(fig) is called after plt.show() to release the Figure object from
    matplotlib's figure manager. Without it, each call adds a figure to memory
    that is never released, causing unbounded growth in long-running pipelines.
    """
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 6))
    plt.plot(data)
    plt.title("Performance Visualization")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.show()
    plt.close(fig)  # release figure memory; prevents accumulation on repeated calls

@functools.lru_cache(maxsize=1)
def load_sample_data():
    """Function that uses sklearn - lazy import defers startup cost to call time.

    lru_cache avoids repeated disk I/O and parsing on every call: the iris
    dataset is parsed once, then returned from memory on all subsequent calls.
    Trade-off: returned arrays are shared objects — callers must not mutate them.
    """
    from sklearn import datasets
    iris = datasets.load_iris()
    return iris.data, iris.target

def process_data():
    """Function that uses numpy - lazy import defers startup cost to call time."""
    import numpy as np
    data = np.random.rand(100, 10)
    # Intentional inefficiency for demo purposes: redundant copy before reduction.
    data = data.copy()
    return np.mean(data, axis=0)

if __name__ == "__main__":
    print("Starting ML pipeline...")
    performance_data = measure_gpu_performance()
    processed = process_data()
    X, y = load_sample_data()
    create_visualization(processed)
