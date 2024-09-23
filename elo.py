import math
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

import reader

INITIAL_ELO = 1000
K_FACTOR = 39  # The K-factor determines the maximum possible change in rating.
HOME_FIELD_ADVANTAGE = 60  # Elo points added to the home team's rating for home advantage - 60 by experiment


def expected_result(elo_a, elo_b):
    return 1 / (1 + math.pow(10, (elo_b - elo_a) / 400))


def update_elo(elo, score, expected):
    return elo + K_FACTOR * (score - expected)


def calculate_elo_ratings(matches):
    total_dif = 0

    clubs, dates = get_clubs_and_matches(matches)
    elo_ratings = {club: INITIAL_ELO for club in clubs}
    arr = [{club: INITIAL_ELO for club in clubs} for _ in range(len(dates))]
    date_index = 0

    for match in matches:
        date, home_club, away_club, home_score, away_score = match
        if date > dates[date_index]:
            # update the current elo ratings as we move to next date
            for club in clubs:
                arr[date_index][club] = elo_ratings[club]

            # and increment date index
            date_index += 1

        if home_club not in elo_ratings:
            elo_ratings[home_club] = INITIAL_ELO
        if away_club not in elo_ratings:
            elo_ratings[away_club] = INITIAL_ELO

        home_elo = elo_ratings[home_club]
        away_elo = elo_ratings[away_club]

        if home_score > away_score:
            home_result = 1
            away_result = 0
        elif home_score < away_score:
            home_result = 0
            away_result = 1
        else:
            home_result = 0.5
            away_result = 0.5

        # calc expected results
        expected_home = expected_result(home_elo + HOME_FIELD_ADVANTAGE, away_elo)
        expected_away = expected_result(away_elo, home_elo + HOME_FIELD_ADVANTAGE)

        # Update Elo ratings
        new_home_elo = update_elo(home_elo, home_result, expected_home)
        new_away_elo = update_elo(away_elo, away_result, expected_away)

        dif = abs(home_result - expected_home)
        total_dif += dif

        if expected_away >= 0.7 and away_result == 1:
            print(home_club, "(", home_elo, ")", home_score, "-", away_score, away_club, "(", away_elo, ")", date)

        # store elo ratings
        elo_ratings[home_club] = new_home_elo
        elo_ratings[away_club] = new_away_elo

    print("total error:", total_dif, "\n")
    return elo_ratings


def get_clubs_and_matches(matches):
    clubs = []
    dates = []
    for match in matches:
        if match[0] not in dates:
            dates.append(match[0])
        if match[1] not in clubs:
            clubs.append(match[1])
        if match[2] not in clubs:
            clubs.append(match[2])
    return clubs, dates


# Example usage:

matches = reader.read_matches("matches.txt")
elo_ratings = calculate_elo_ratings(matches)
for elo_rating in elo_ratings:
    print(elo_rating, elo_ratings[elo_rating])

