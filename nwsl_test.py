from datetime import datetime
import reader
import elo

FIRST_DATE = datetime(2013, 4, 13)
FINAL_DATE = datetime.today()
club_metadata = {
    "Kansas City": (FIRST_DATE, datetime(2017, 12, 31), "#A7D4E9"),
    "Thorns": (FIRST_DATE, FINAL_DATE, "#006225"),
    "Gotham": (FIRST_DATE, FINAL_DATE, "#A7F1F6"),
    "Courage": (FIRST_DATE, FINAL_DATE, "#B8A569"),
    "Boston": (FIRST_DATE, datetime(2017, 12, 31), "#CFD7E7"),
    "Spirit": (FIRST_DATE, FINAL_DATE, "#EDEA39"),
    "Red Stars": (FIRST_DATE, FINAL_DATE, "#D3152A"),
    "Reign": (FIRST_DATE, FINAL_DATE, "#979DA3"),
    "Dash": (datetime(2014, 1, 1), FINAL_DATE, "#F46D1C"),
    "Pride": (datetime(2016, 1, 1), FINAL_DATE, "#643095"),
    "Royals": (datetime(2018, 1, 1), FINAL_DATE, "#FDB71B"),
    "Current": (datetime(2021, 1, 1), FINAL_DATE, "#63CCCA"),
    "Louisville": (datetime(2021, 1, 1), FINAL_DATE, "#C9B5F6"),
    "Angel City": (datetime(2022, 1, 1), FINAL_DATE, "#EB8F83"),
    "Wave": (datetime(2022, 1, 1), FINAL_DATE, "#FD0F97"),
    "Bay FC": (datetime(2024, 1, 1), FINAL_DATE, "#041A2E"),
}

hfa = 45
k = 30
sr = 0.5511
matches = reader.read_matches("nwsl_matches.txt")
elo_ratings, arr, dates, total_results, dif = elo.calculate_elo_ratings(matches, print_error=False,
                                                                        home_field_advantage=hfa, k=k,
                                                                        season_reset=sr,
                                                                        end_date=datetime(2028, 10, 22),
                                                                        reset_date=datetime(1, 1, 1))

# if season_reset, k=33, hfa=44
# if no season_reset, k=25, hfa=44

# with variable sr:
# k=30, hfa=45, sr=0.55

# for elo_rating in elo_ratings:
#     print(elo_rating, ":", elo_ratings[elo_rating])
#
sorted_elos = sorted(elo_ratings, key=elo_ratings.get)
# sorted_elos.reverse()
# for elo_rating in sorted_elos:
#     if elo_rating not in ["Boston", "Kansas City"]:
#         print(elo_rating)
#         print(elo_rating, elo_ratings[elo_rating])

# number = 44.5

clubs, _ = elo.get_clubs_and_matches(matches)
elo.plot_elo_ratings_over_time(arr, dates, clubs, club_metadata=club_metadata)

# home = "Gotham"
# away = "Pride"
# print(str(elo_ratings[home]) + ", " + str(elo_ratings[away]))
# print(elo.expected_result(elo_ratings[home] + hfa, elo_ratings[away]))
