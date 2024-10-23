import random
import elo
import reader

matches = reader.read_matches("nwsl_matches.txt")

# Define the search ranges
hfa_range = (0, 100)
k_range = (1, 100)
sr_range = (0, 1)

best_dif = float('inf')
best_hfa = None
best_k = None
best_sr = None

for i in range(100000):  # Run random search for 1000 iterations
    hfa = random.randint(*hfa_range)
    k = random.randint(*k_range)
    sr = random.uniform(*sr_range)  # Float between 0 and 1

    # Calculate the Elo ratings and difference for the current parameters
    elo_ratings, arr, dates, total_results, dif = elo.calculate_elo_ratings(matches,
                                                                            initial_elo=1000,
                                                                            home_field_advantage=hfa,
                                                                            k=k,
                                                                            print_error=False,
                                                                            season_reset=sr)
    # Check if we have a new best
    if dif < best_dif:
        best_dif = dif
        best_hfa = hfa
        best_k = k
        best_sr = sr
        print(f"Best so far -> HFA: {best_hfa}, K: {best_k}, SR: {best_sr}, Dif: {best_dif}")

# Output the final best parameters
print(f"Optimal Parameters -> HFA: {best_hfa}, K: {best_k}, SR: {best_sr}, Dif: {best_dif}")
