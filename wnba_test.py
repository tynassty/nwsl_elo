from datetime import datetime

import reader
import elo

FIRST_DATE = datetime(2013, 4, 13)
FINAL_DATE = datetime.today()
club_metadata = {
    "Atlanta Dream": (FIRST_DATE, FINAL_DATE, "#418FDE"),
    "Chicago Sky": (FIRST_DATE, FINAL_DATE, "#FFCD00"),
    "Connecticut Sun": (FIRST_DATE, FINAL_DATE, "#DC4405"),
    "Dallas Wings": (FIRST_DATE, FINAL_DATE, "#c4d600"),
    "Indiana Fever": (FIRST_DATE, FINAL_DATE, "#C8102E"),
    "Las Vegas Aces": (FIRST_DATE, FINAL_DATE, "#A6A8AA"),
    "Los Angeles Sparks": (FIRST_DATE, FINAL_DATE, "#702F8A"),
    "Minnesota Lynx": (FIRST_DATE, FINAL_DATE, "#78BE20"),
    "New York Liberty": (FIRST_DATE, FINAL_DATE, "#6ECEB2"),
    "Phoenix Mercury": (FIRST_DATE, FINAL_DATE, "#CB6015"),
    "Seattle Storm": (FIRST_DATE, FINAL_DATE, "#2C5234"),
    "Washington Mystics": (FIRST_DATE, FINAL_DATE, "#0c2340"),
}

hfa = 24
k = 40
sr = 0.4240
matches = reader.read_matches("wnba_matches.txt")
elo_ratings, arr, dates, total_results, dif = elo.calculate_elo_ratings(matches, print_error=True,
                                                                        home_field_advantage=hfa, k=k,
                                                                        season_reset=sr,
                                                                        end_date=datetime(2029, 10, 15))

# if season_reset, k=33, hfa=44
# if no season_reset, k=25, hfa=44

# for elo_rating in elo_ratings:
#     print(elo_rating, ":", elo_ratings[elo_rating])
#
sorted_elos = sorted(elo_ratings, key=elo_ratings.get)
sorted_elos.reverse()
# for elo_rating in sorted_elos:
#     if elo_ratings[elo_rating] != 1000:
#         print(elo_rating)
#         print(elo_rating, elo_ratings[elo_rating])

# number = 44.5

clubs, _ = elo.get_clubs_and_matches(matches)
elo.plot_elo_ratings_over_time(arr, dates, clubs, club_metadata=club_metadata)

# home = "Pride"
# away = "Reign"
# print(str(elo_ratings[home]) + ", " + str(elo_ratings[away]))
# print(elo.expected_result(elo_ratings[home] + hfa, elo_ratings[away]))
