import random
from datetime import datetime

import elo
import reader
import table


def calculate_probs(expected_result):
    """
    Calculates the probabilities for win, draw, and loss outcomes given the expected result.

    :param expected_result: Expected probability of the home team winning, typically derived from Elo ratings.
    :return: Tuple containing probabilities for win, draw, and loss outcomes in that order.
    """
    draw = -1.008241359 * ((expected_result ** 2) - expected_result)
    win = expected_result - (draw/2)
    loss = 1 - win - draw
    return win, draw, loss


def print_wdl(wdl):
    """
    Prints the win, draw, and loss probabilities as percentages with two decimal places.

    :param wdl: Tuple containing win, draw, and loss probabilities.
    """
    print(f"Win: {wdl[0]*100:.2f}% Draw: {wdl[1]*100:.2f}% Loss: {wdl[2]*100:.2f}%")


if __name__ == "__main__":
    matches = reader.read_matches_obj("nwsl_matches.txt")
    today = datetime(2028, 10, 31)
    completed_matches = [match for match in matches if match.date < today]
    incomplete_matches = [match for match in matches if match.date >= today]
    hfa = 45
    k = 30
    sr = 0.5511
    elo_ratings, arr, dates, total_results, dif = elo.calculate_elo_ratings(completed_matches, print_error=False,
                                                                            home_field_advantage=hfa, k=k,
                                                                            season_reset=sr,
                                                                            end_date=datetime(2028, 10, 22),
                                                                            reset_date=datetime(1, 1, 1))

    nwsl_table = table.LeagueTable()
    for match in completed_matches:
        if match.date.year == 2013 and match.regular_season is True:
            nwsl_table.record_match(match.home_club, match.away_club, match.home_score, match.away_score)

    nwsl_table.deduct_points("Angel City", 3)
    # nwsl_table.standings()
    print()

    for match in incomplete_matches:
        random_number = random.random()
        expected_result = elo.expected_result(elo_ratings[match[1]] + hfa, elo_ratings[match[2]])
        win, draw, loss = calculate_probs(expected_result)
        if win > random_number:
            nwsl_table.record_match(match[1], match[2], 2, 0)
        elif win+draw > random_number:
            nwsl_table.record_match(match[1], match[2], 1, 1)
        else:
            nwsl_table.record_match(match[1], match[2], 0, 2)

    # nwsl_table.standings()
    print(nwsl_table)

        # print(f"Date: {match[0].year}-{match[0].month}-{match[0].day}, Home: {match[1]}, Away: {match[2]}")
        # print_wdl(calculate_probs(expected_result))
    # expected_result = elo.expected_result(elo_ratings["Pride"] + hfa, elo_ratings["Gotham"])
    # print(expected_result)
    # wdl = calculate_probs(expected_result)
    # print_wdl(wdl)

