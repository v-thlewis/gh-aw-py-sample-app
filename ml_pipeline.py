"""
ML pipeline module. Heavy dependencies (torch, numpy, matplotlib, sklearn)
are loaded lazily inside each function to minimise startup cost and memory.
"""


def measure_gpu_performance():
    """Function that uses torch - lazy import defers startup cost to call time."""
    import torch
    import numpy as np
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tensor = torch.randn(1000, 1000, device=device)
    result = torch.matmul(tensor, tensor.t())
    return result.cpu().numpy()

def create_visualization(data):
    """Function that uses matplotlib - lazy import defers startup cost to call time."""
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.plot(data)
    plt.title("Performance Visualization")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.show()

def load_sample_data():
    """Function that uses sklearn - lazy import defers startup cost to call time."""
    from sklearn import datasets
    iris = datasets.load_iris()
    return iris.data, iris.target

def process_data():
    """Function that uses numpy - lazy import defers startup cost to call time."""
    import numpy as np
    data = np.random.rand(100, 10)
    return np.mean(data, axis=0)

if __name__ == "__main__":
    print("Starting ML pipeline...")
    performance_data = measure_gpu_performance()
    processed = process_data()
    X, y = load_sample_data()
    create_visualization(processed)
