import random

import datetime
import elo
import reader

matches = reader.read_matches("ncaaf_matches.txt")

hfa = 60
k = 40
sr = 0.5

best_dif = float('inf')
best_hfa = 60
best_k = 40
best_sr = 0

for k in range(76, 77, 1):
    for hfa in range(64, 65, 1):
        for sr in range(1940, 1960):
            sr_frac = sr/100000
            _, _, _, _, dif = elo.calculate_elo_ratings(matches,
                                                        initial_elo=1000,
                                                        home_field_advantage=hfa,
                                                        k=k,
                                                        print_error=False,
                                                        season_reset=sr_frac,
                                                        reset_date=datetime.datetime(1, 3, 1))
            if dif < best_dif:
                best_dif = dif
                best_hfa = hfa
                best_k = k
                best_sr = sr_frac
                print(str(best_hfa) + ", " + str(best_k) + ", " + str(best_sr) + " -- " + str(best_dif))
            else:
                print("x --- " + str(hfa) + ", " + str(k) + ", " + str(sr))
                print(str(best_hfa) + ", " + str(best_k) + ", " + str(best_sr) + " -- " + str(best_dif))


# nwsl no reset vanilla: (72, 52)
