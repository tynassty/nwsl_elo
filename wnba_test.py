from datetime import datetime

import reader
import elo

FIRST_DATE = datetime(1997, 1, 1)
FINAL_DATE = datetime.today()
club_metadata = {
    "Atlanta Dream": (datetime(2008, 1, 1), FINAL_DATE, "#418FDE"),
    "Chicago Sky": (datetime(2006, 1, 1), FINAL_DATE, "#FFCD00"),
    "Connecticut Sun": (datetime(1999, 1, 1), FINAL_DATE, "#DC4405"),
    "Dallas Wings": (datetime(1998, 1, 1), FINAL_DATE, "#c4d600"),
    "Indiana Fever": (datetime(2000, 1, 1), FINAL_DATE, "#C8102E"),
    "Las Vegas Aces": (FIRST_DATE, FINAL_DATE, "#A6A8AA"),
    "Los Angeles Sparks": (FIRST_DATE, FINAL_DATE, "#702F8A"),
    "Minnesota Lynx": (datetime(1999, 1, 1), FINAL_DATE, "#78BE20"),
    "New York Liberty": (FIRST_DATE, FINAL_DATE, "#6ECEB2"),
    "Phoenix Mercury": (FIRST_DATE, FINAL_DATE, "#CB6015"),
    "Seattle Storm": (datetime(2000, 1, 1), FINAL_DATE, "#2C5234"),
    "Washington Mystics": (datetime(1998, 1, 1), FINAL_DATE, "#0c2340"),
    "Cleveland Rockers": (FIRST_DATE, datetime(2004, 1, 1), "#041922"),
    "Charlotte Sting": (FIRST_DATE, datetime(2007, 1, 1), "#025A89"),
    "Houston Comets": (FIRST_DATE, datetime(2009, 1, 1), "#00265D"),
    "Sacramento Monarchs": (FIRST_DATE, datetime(2010, 1, 1), "#363996"),
    "Miami Sol": (datetime(2000, 1, 1), datetime(2003, 1, 1), "#F49D35"),
    "Portland Fire": (datetime(2000, 1, 1), datetime(2003, 1, 1), "#E2A516"),
}

hfa = 70
k = 32
sr = 0.4777
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

# clubs, _ = elo.get_clubs_and_matches(matches)
# elo.plot_elo_ratings_over_time(arr, dates, clubs, club_metadata=club_metadata)

# home = "Pride"
# away = "Reign"
# print(str(elo_ratings[home]) + ", " + str(elo_ratings[away]))
# print(elo.expected_result(elo_ratings[home] + hfa, elo_ratings[away]))
