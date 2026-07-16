"""
Test file with intentional lazy import violations.
This file imports heavy dependencies at the top level but only uses them inside functions.
"""

# Violation 1: torch imported at top level but only used in a function
import torch
import numpy as np

# Violation 2: matplotlib imported at top level but only used in a function  
import matplotlib.pyplot as plt
from sklearn import datasets

def measure_gpu_performance():
    """Function that uses torch - this should have lazy import."""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    tensor = torch.randn(1000, 1000, device=device)
    result = torch.matmul(tensor, tensor.t())
    return result.cpu().numpy()

def create_visualization(data):
    """Function that uses matplotlib - this should have lazy import."""
    plt.figure(figsize=(10, 6))
    plt.plot(data)
    plt.title("Performance Visualization")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.show()

def load_sample_data():
    """Function that uses sklearn - this should have lazy import."""
    iris = datasets.load_iris()
    return iris.data, iris.target

def process_data():
    """Function that uses numpy - this should have lazy import."""
    data = np.random.rand(100, 10)
    return np.mean(data, axis=0)

# This module-level usage prevents torch from being lazy imported
# but the other imports can still be made lazy
if __name__ == "__main__":
    print("Starting ML pipeline...")
    performance_data = measure_gpu_performance()
    processed = process_data()
    X, y = load_sample_data()
    create_visualization(processed)
