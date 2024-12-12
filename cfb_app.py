import datetime

import elo
import ncaaf_test
import reader

matches = reader.read_matches("ncaaf_matches.txt")
hfa = 65
elo_ratings, arr, dates, total_results, dif \
    = elo.calculate_elo_ratings(matches, initial_elo=1000, home_field_advantage=hfa, k=76, season_reset=False,
                                end_date=datetime.datetime(2029, 3, 1), print_error=False)

# # by test, if k=100m hfa=312(!!)

# for elo_rating in elo_ratings:
#     print(elo_rating, elo_ratings[elo_rating])

sorted_elos = sorted(elo_ratings, key=elo_ratings.get)
sorted_elos.reverse()
# for i in range(25):
#     print(sorted_elos[i])

# for i in range(len(sorted_elos)):
#     print(i+1, sorted_elos[i], elo_ratings[sorted_elos[i]])

# print(elo_ratings["Syracuse"])

# # by test, k=76 if hfa=0
# # by test, if k=76, hfa=65

clubs = []

while True:
    club_input = input("Enter clubs (or 'exit' to quit): ")
    if club_input.lower() == 'exit':
        break

    if club_input and club_input[0] == "+":
        club_input = club_input[1:]
    else:
        clubs = []

    if club_input == "ACC":
        clubs = ncaaf_test.ACC
        club_input = ""
    elif club_input == "OLD_PAC":
        clubs = ncaaf_test.OLD_PAC
        club_input = ""

    clubs.extend(ncaaf_test.parse_csv_with_commas(club_input))

    elo.plot_elo_ratings_over_time(arr, dates, clubs)
