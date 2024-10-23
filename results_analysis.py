import reader
import elo
from datetime import datetime

# ncaaf
hfa = 64
k = 75

# NWSL
# hfa = 44
# k = 25

matches = reader.read_matches("ncaaf.txt")
elo_ratings, arr, dates, total_results, dif = elo.calculate_elo_ratings(matches, print_error=True,
                                                                        home_field_advantage=hfa, k=k,
                                                                        season_reset=False,
                                                                        end_date=datetime(2059, 10, 15))
bin_ct = 20
bins = [i/bin_ct for i in range(bin_ct)]
bins.extend([1])
# bin_sum = [0 for i in range(bin_ct)]
print(bins)
results = [[0 for i in range(len(bins))] for j in range(3)]
# print(results)

for i in range(len(total_results[0])):
    exp_home = total_results[0][i]
    act_home = total_results[1][i]
    for j in range(len(bins) - 1):
        if bins[j] <= exp_home < bins[j+1]:
            # bin_sum[j] += 1
            if act_home == 1:
                results[0][j] += 1
            elif act_home == 0.5:
                results[1][j] += 1
            else:
                results[2][j] += 1
print(results)
# print(bin_sum)

