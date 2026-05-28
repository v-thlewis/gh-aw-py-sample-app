"""
ML pipeline with lazy imports so heavy dependencies are only loaded when actually used.
"""


def measure_gpu_performance():
    """Function that uses torch."""
    import torch
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tensor = torch.randn(1000, 1000, device=device)
    result = torch.matmul(tensor, tensor.t())
    return result.cpu().numpy()

def create_visualization(data):
    """Function that uses matplotlib."""
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.plot(data)
    plt.title("Performance Visualization")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.show()

def load_sample_data():
    """Function that uses sklearn."""
    from sklearn import datasets
    iris = datasets.load_iris()
    return iris.data, iris.target

def process_data():
    """Function that uses numpy."""
    import numpy as np
    data = np.random.rand(100, 10)
    return np.mean(data, axis=0)

if __name__ == "__main__":
    print("Starting ML pipeline...")
    performance_data = measure_gpu_performance()
    processed = process_data()
    X, y = load_sample_data()
    create_visualization(processed)
