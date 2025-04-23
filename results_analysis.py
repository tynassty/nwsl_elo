import reader
import elo
from datetime import datetime

# ncaaf
# hfa = 60
# k = 78
# sr = 0.0125
# rd = datetime(1, 3, 1)

# NWSL
hfa = 45
k = 32
sr = 0.5511
rd = datetime(1, 1, 1)

# WNBA
# hfa = 70
# k = 32
# sr = 0.4777
# rd = datetime(1, 1, 1)

matches = reader.read_matches_obj("nwsl_matches.txt")
matches = [match for match in matches if match.date <= datetime.today()]
elo_ratings, arr, dates, total_results, dif = elo.calculate_elo_ratings(matches, print_error=False,
                                                                        home_field_advantage=hfa, k=k,
                                                                        season_reset=sr,
                                                                        end_date=datetime(2028, 10, 22),
                                                                        reset_date=rd)
bin_ct = 20
bins = [i/bin_ct for i in range(bin_ct)]
bins.extend([1])
# bin_sum = [0 for i in range(bin_ct)]
print(bins)
results = [[0 for i in range(len(bins))] for j in range(9)]
# print(results)

for i in range(len(total_results[0])):
    exp_home = total_results[0][i]
    act_home = total_results[1][i]
    for j in range(len(bins) - 1):
        if bins[j] <= exp_home < bins[j+1]:
            # if act_home == 1:
            #     results[0][j] += 1
            # elif act_home == 0.5:
            #     results[1][j] += 1
            # else:
            #     results[2][j] += 1
            margin = matches[i].home_score - matches[i].away_score + 4
            margin = min(max(margin, 0), 8)
            # print(matches[i], margin)
            results[margin][j] += 1
# print(results)
for result in results:
    print(result)
# print(bin_sum)

