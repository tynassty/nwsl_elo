import csv
import datetime
import elo
import reader

ACC = ["Florida State", "Louisville", "North Carolina State", "Georgia Tech", "Virginia Tech", "North Carolina",
       "Clemson", "Duke", "Miami (FL)", "Boston College", "Syracuse", "Virginia", "Pittsburgh", "Wake Forest",
       "Southern Methodist", "California", "Stanford"]
OLD_ACC = ["Florida State", "Louisville", "North Carolina State", "Georgia Tech", "Virginia Tech", "North Carolina",
           "Clemson", "Duke", "Miami (FL)", "Boston College", "Syracuse", "Virginia", "Pittsburgh", "Wake Forest"]
CLASSIC_ACC = ["Clemson", "Duke", "Maryland", "North Carolina", "North Carolina State", "Wake Forest", "Virginia",
               "Georgia Tech", "Florida State"]
SEC = ["Texas", "Oklahoma", "Florida", "Georgia", "Vanderbilt", "Kentucky", "Missouri", "Texas A&M", "Arkansas",
       "Louisiana State", "Tennessee", "Mississippi", "Mississippi State", "Auburn", "Alabama", "South Carolina"]
SEC_E = ["Kentucky", "Tennessee", "Florida", "Georgia", "Missouri", "Vanderbilt", "South Carolina"]
SEC_W = ["Alabama", "Louisiana State", "Mississippi", "Texas A&M", "Auburn", "Arkansas", "Mississippi State"]
MAC = ["Buffalo", "Eastern Michigan", "Central Michigan", "Ohio", "Toledo", "Bowling Green", "Miami (OH)",
       "Western Michigan", "Northern Illinois", "Ball State", "Akron", "Kent State"]
CLASSIC_BIGEAST = ["Miami (FL)", "West Virginia", "Pittsburgh", "Virginia Tech", "Boston College", "Temple",
                   "Syracuse", "Rutgers"]
OLD_PAC_NORTH = ["Washington", "Oregon State", "Oregon", "Washington State", "California", "Stanford"]
OLD_PAC_SOUTH = ["Southern California", "UCLA", "Utah", "Arizona", "Arizona State", "Colorado"]
OLD_PAC = OLD_PAC_NORTH + OLD_PAC_SOUTH


def parse_csv_with_commas(input_string):
    # Use csv.reader to correctly handle commas within quotes
    csv_reader = csv.reader([input_string], quotechar='"', delimiter=',', skipinitialspace=True)
    return next(csv_reader)  # Return the first row as a list


if __name__ == "__main__":
    matches = reader.read_matches("ncaaf.txt")
    hfa = 64
    elo_ratings, arr, dates, total_results, dif \
        = elo.calculate_elo_ratings(matches, initial_elo=1000, home_field_advantage=hfa, k=76, season_reset=0.01954,
                                    end_date=datetime.datetime(2024, 10, 21), print_error=False,
                                    reset_date=datetime.datetime(1, 3, 1))

    # hfa=64, k=75

    # sr=0.01954, hfa=64, k=76

    # for elo_rating in elo_ratings:
    #     print(elo_rating, elo_ratings[elo_rating])

    sorted_elos = sorted(elo_ratings, key=elo_ratings.get)
    sorted_elos.reverse()
    # for i in range(25):
    #     print(sorted_elos[i])

    # for i in range(len(sorted_elos)):
    #     print(i+1, sorted_elos[i], elo_ratings[sorted_elos[i]])

    # print(elo_ratings["Syracuse"])
    # clubs = SEC_E
    # elo.plot_elo_ratings_over_time(arr, dates, clubs, block=False)

    clubs = SEC_W
    elo.plot_elo_ratings_over_time(arr, dates, clubs)

    # print(elo.expected_result(elo_ratings["Pittsburgh"] + hfa, elo_ratings["Syracuse"]))
    # print(a)
    # print(elo.update_elo(elo_ratings["Syracuse"], 1, a))
