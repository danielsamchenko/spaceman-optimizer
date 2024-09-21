import numpy as np

def optimal_multiplier(crash_multipliers, k=1):
    average_multiplier = np.mean(crash_multipliers)
    standard_deviation = np.std(crash_multipliers)
    optimal_multiplier = average_multiplier + k * standard_deviation
    return optimal_multiplier

# Example usage:
crash_multipliers = [1.5, 2.0, 1.8, 3.0, 2.5, 1.2, 2.8]
k = 1  # Adjust this value based on your risk tolerance
print(optimal_multiplier(crash_multipliers, k))
