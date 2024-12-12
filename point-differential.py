# import reader
#
# matches = reader.read_matches("ncaaf_matches.txt")
# for match in matches:
#     print(match[0])
# print(len(matches))

# Recalculate the bounds based on the new expressions for p_L and p_D
# Lower bound: p_W >= max(2X - 1, 0)
# Upper bound: p_W <= min(2X, 1)

# Lower bound calculation: max(2X - 1, 0)
import numpy as np
from matplotlib import pyplot as plt

X_values = np.linspace(0, 1, 1000)

p_W_lower = np.maximum(2 * X_values - 1, 0)

# Upper bound calculation: min(2X, 1)
p_W_upper = np.minimum(2 * X_values, 1)

p_W_midpoint = (p_W_upper + p_W_lower) / 2

# Plotting the recalculated bounds
plt.figure(figsize=(8, 6))
plt.plot(X_values, p_W_upper, label="Upper bound of p_W", color='blue')
plt.plot(X_values, p_W_lower, label="Lower bound of p_W", color='red')
plt.plot(X_values, p_W_midpoint, label="Midpoint of p_W", color='green', linestyle='--')
plt.fill_between(X_values, p_W_lower, p_W_upper, color='gray', alpha=0.3)

# Add labels and title
plt.xlabel("Expected Value (X)")
plt.ylabel("p_W")
plt.title("Recalculated Upper and Lower Bounds of p_W for Different Expected Values (X)")
plt.legend()

# Show plot
plt.grid(True)
plt.show()
