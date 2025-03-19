import random
from datetime import datetime

import nwsl_simulator
import reader
import elo

BIG_SIX = ["Manchester City", "Manchester Utd", "Liverpool", "Arsenal", "Chelsea", "Tottenham"]

FIRST_DATE = datetime(2013, 4, 13)
FINAL_DATE = datetime.today()
club_metadata = {

}

hfa = 45
k = 21
sr = 0.0000
matches = []
matches += reader.read_matches_obj("efl_matches/epl_matches.txt")
matches += reader.read_matches_obj("efl_matches/eflc_matches.txt")
matches += reader.read_matches_obj("efl_matches/efl1_matches.txt")
matches += reader.read_matches_obj("efl_matches/efl2_matches.txt")
matches += reader.read_matches_obj("efl_matches/eflcup_matches.txt")
matches += reader.read_matches_obj("efl_matches/natl_matches.txt")
matches = sorted(matches)
elo_ratings, arr, dates, total_results, dif = elo.calculate_elo_ratings(matches, print_error=False,
                                                                        home_field_advantage=hfa, k=k,
                                                                        season_reset=sr,
                                                                        end_date=datetime(2028, 10, 22),
                                                                        reset_date=datetime(1, 7, 1))

# if season_reset, k=33, hfa=44
# if no season_reset, k=25, hfa=44

# with variable sr:
# k=30, hfa=45, sr=0.55

# for elo_rating in elo_ratings:
#     print(elo_rating, ":", elo_ratings[elo_rating])
#
sorted_elos = sorted(elo_ratings, key=elo_ratings.get)
sorted_elos.reverse()
# print(elo_ratings["FG Rovers"])
# for i in range(len(sorted_elos)):
#     print(i, sorted_elos[i], elo_ratings[sorted_elos[i]])
# for elo_rating in sorted_elos:
#     if elo_rating not in ["Boston", "Kansas City"]:
#         print(elo_rating)
#         print(elo_rating, elo_ratings[elo_rating])

# number = 44.5

clubs = BIG_SIX
# clubs, _ = elo.get_clubs_and_matches(matches)
elo.plot_elo_ratings_over_time(arr, dates, clubs, club_metadata=club_metadata)

# home = "Current"
# away = "Courage"
# print(str(elo_ratings[home]) + ", " + str(elo_ratings[away]))
# expected_result = elo.expected_result(elo_ratings[home] + hfa, elo_ratings[away])
# nwsl_simulator.print_wdl(nwsl_simulator.calculate_probs(expected_result))
# print(expected_result)
