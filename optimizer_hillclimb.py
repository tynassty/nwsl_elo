import datetime
import random
import elo
import reader

matches = reader.read_matches("wnba_matches.txt")

# Define maximum ranges
hfa_range = (0, 100)
k_range = (1, 100)
sr_range = (0, 1)

# Define initial parameters
current_hfa = random.randint(hfa_range[0], hfa_range[1])
current_k = random.randint(k_range[0], k_range[1])
current_sr = random.uniform(sr_range[0], sr_range[1])
best_dif = float('inf')


def calculate_dif(hfa, k, sr):
    _, _, _, _, dif = elo.calculate_elo_ratings(matches,
                                                initial_elo=1000,
                                                home_field_advantage=hfa,
                                                k=k,
                                                print_error=False,
                                                season_reset=sr,
                                                reset_date=datetime.datetime(1, 1, 1))
    return dif


# Hill Climbing Algorithm
for iteration in range(10000):  # Limit the number of iterations
    # Generate neighbors by tweaking parameters slightly
    neighbor_hfa = current_hfa + random.randint(-5, 5)
    neighbor_k = current_k + random.randint(-5, 5)
    neighbor_sr = current_sr + random.uniform(-0.01, 0.01)

    # Ensure neighbors are within bounds
    neighbor_hfa = max(hfa_range[0], min(hfa_range[1], neighbor_hfa))
    neighbor_k = max(k_range[0], min(k_range[1], neighbor_k))
    neighbor_sr = max(sr_range[0], min(sr_range[1], neighbor_sr))

    # Calculate the difference for the neighbor parameters
    neighbor_dif = calculate_dif(neighbor_hfa, neighbor_k, neighbor_sr)

    # If the neighbor is better, move to the neighbor
    if neighbor_dif < best_dif:
        current_hfa = neighbor_hfa
        current_k = neighbor_k
        current_sr = neighbor_sr
        best_dif = neighbor_dif
        print(f"Improved -> HFA: {current_hfa}, K: {current_k}, SR: {current_sr:.4f}, Dif: {best_dif:.10f}")

# Output the final best parameters
print(f"Optimal Parameters -> HFA: {current_hfa}, K: {current_k}, SR: {current_sr:.4f}, Dif: {best_dif:.10f}")
