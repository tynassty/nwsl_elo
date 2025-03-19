import datetime
import random
import elo
import reader

matches = []
# matches += reader.read_matches_obj("efl_matches/epl_matches.txt")
# matches += reader.read_matches_obj("efl_matches/eflc_matches.txt")
# matches += reader.read_matches_obj("efl_matches/efl1_matches.txt")
# matches += reader.read_matches_obj("efl_matches/efl2_matches.txt")
# matches += reader.read_matches_obj("efl_matches/eflcup_matches.txt")
# matches += reader.read_matches_obj("efl_matches/natl_matches.txt")
# matches += reader.read_matches_obj("ncaaf_matches.txt")
matches += reader.read_matches_obj("nwsl_matches.txt")
matches = sorted(matches)
print("Total matches:", len(matches))
# matches = [match for match in matches if match[0].year > 2015]
reset_date = datetime.datetime(1, 3, 1)

# Define maximum ranges
hfa_range = (0, 100)
k_range = (1, 100)
sr_range = (0, 1)

# Define initial parameters
current_hfa = random.randint(hfa_range[0], hfa_range[1])
current_k = random.randint(k_range[0], k_range[1])
current_sr = random.uniform(sr_range[0], sr_range[1])
# current_sr = 0.5511
best_dif = float('inf')

max_iterations = 10000


def calculate_dif(hfa, k, sr):
    _, _, _, _, dif = elo.calculate_elo_ratings(matches,
                                                initial_elo=1000,
                                                home_field_advantage=hfa,
                                                k=k,
                                                print_error=False,
                                                season_reset=sr,
                                                end_date=datetime.datetime.today(),
                                                reset_date=reset_date)
    return dif


# Hill Climbing Algorithm
for iteration in range(max_iterations):  # Limit the number of iterations
    # Reduce step size as iterations progress
    step_factor = 1 - (iteration/max_iterations)

    # Generate neighbors by tweaking parameters slightly
    neighbor_hfa = current_hfa + int(random.randint(-5, 5) * step_factor)
    neighbor_k = current_k + int(random.randint(-5, 5) * step_factor)
    neighbor_sr = current_sr + random.uniform(-0.05, 0.05) * step_factor

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
        print(f"Improved -> HFA: {current_hfa}, K: {current_k}, SR: {current_sr:.4f}, Dif: {best_dif:.10f}, "
              f"Iteration: {iteration}")
        # print(step_factor)

# Output the final best parameters
print(f"Optimal Parameters -> HFA: {current_hfa}, K: {current_k}, SR: {current_sr:.4f}, Dif: {best_dif:.10f}")
