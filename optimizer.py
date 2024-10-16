import random

import elo
import reader

matches = reader.read_matches("matches.txt")

hfa = 60
k = 40

best_dif = float('inf')
best_hfa = 60
best_k = 40

for k in range(25, 26, 1):
    for hfa in range(0, 100, 1):
        elo_ratings, arr, dates, total_results, dif = elo.calculate_elo_ratings(matches, initial_elo=1000,
                                                                                home_field_advantage=hfa, k=k,
                                                                                print_error=False,
                                                                                season_reset=False)
        if dif < best_dif:
            best_dif = dif
            best_hfa = hfa
            best_k = k
            print(best_dif)
            print(best_hfa, ",", best_k)


# nwsl no reset vanilla: (72, 52)
