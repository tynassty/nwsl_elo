import csv
from datetime import datetime
import elo
import reader
import random
import ncaaf_metadata as md


def parse_csv_with_commas(input_string):
    # Use csv.reader to correctly handle commas within quotes
    csv_reader = csv.reader([input_string], quotechar='"', delimiter=',', skipinitialspace=True)
    return next(csv_reader)  # Return the first row as a list


def calculate_potential_elo(home, away):
    home_elo = elo_ratings[home]
    away_elo = elo_ratings[away]
    print(home_elo)
    print(away_elo)
    home_exp = elo.expected_result(home_elo + hfa, away_elo)
    away_exp = 1 - home_exp
    print(home_exp)
    print(elo.update_elo(home_elo, 1, home_exp, k), ":", elo.update_elo(home_elo, 0, home_exp, k))
    print(elo.update_elo(away_elo, 1, away_exp, k), ":", elo.update_elo(away_elo, 0, away_exp, k))


if __name__ == "__main__":
    matches = reader.read_matches_obj("ncaaf_matches.txt")
    hfa = 60
    k = 77
    sr = 0.0126
    elo_ratings, arr, dates, total_results, dif \
        = elo.calculate_elo_ratings(matches, initial_elo=1000, home_field_advantage=hfa, k=k, season_reset=sr,
                                    end_date=datetime(2024, 12, 30), print_error=False,
                                    reset_date=datetime(1, 3, 1))

    # hfa = 60
    # k = 78
    # sr = 0.0125

    # for elo_rating in elo_ratings:
    #     print(elo_rating, elo_ratings[elo_rating])

    sorted_elos = sorted(elo_ratings, key=elo_ratings.get)
    sorted_elos.reverse()
    # for i in range(len(sorted_elos)):
    #     if sorted_elos[i] in md.AAC_CURRENT:
    #         print(sorted_elos[i])
    # for i in range(25):
    #     print(sorted_elos[i])

    # for i in range(len(sorted_elos)):
    #     print(i+1, sorted_elos[i], elo_ratings[sorted_elos[i]])

    # calculate_potential_elo("Syracuse", "Pittsburgh")

    # clubs = md.ACC
    # elo.plot_elo_ratings_over_time(arr, dates, clubs, club_metadata=md.acc_metadata)
    # clubs = md.B10_CURRENT
    clubs = ["Kansas State", "Northern Illinois"]
    elo.plot_elo_ratings_over_time(arr, dates, clubs)

    # home = "Clemson"
    # away = "Syracuse"
    # print(str(elo_ratings[home]) + ", " + str(elo_ratings[away]))
    # expected_result = elo.expected_result(elo_ratings[home] + hfa, elo_ratings[away])
    # if random.random() > expected_result:
    #     print(away)
    # else:
    #     print(home)
    # print(expected_result)

    # clubs_to_test = md.SEC_CURRENT
    # for i in range(len(clubs_to_test)):
    #     opps = []
    #     matches_2024 = [match for match in matches if match.date.year == 2024 and match.date.month >= 3]
    #     this_club = clubs_to_test[i]
    #     for match in matches_2024:
    #         clubs_in_match = [match.home_club, match.away_club]
    #         if this_club in clubs_in_match:
    #             opps += [item for item in clubs_in_match if item != this_club]
    #     print(opps)
    #
    #     opps_sum = 0
    #     for club in opps:
    #         opps_sum += elo_ratings[club]
    #     print(clubs_to_test[i])
    #     print(opps_sum/len(opps))
