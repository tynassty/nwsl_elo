import math
import random

import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from datetime import timedelta
import reader
import numpy as np

INITIAL_ELO = 1000
HOME_FIELD_ADVANTAGE = 72  # Elo points added to the home team's rating for home advantage (72)
K_FACTOR = 52  # The K-factor determines the (NORMAL) maximum possible change in rating. (52)
WINDOWS = [10, 31, 365]
WINDOW_WEIGHTS = [0, 0, 0]


def expected_result(elo_a, elo_b):
    """
    Calculate the expected result of a match based on the Elo ratings of each club
    :param elo_a: Elo rating of first club
    :param elo_b: Elo rating of second club
    :return: Expected result for first club
    """
    return 1 / (1 + math.pow(10, (elo_b - elo_a) / 400))


def update_elo(elo, score, expected, k=K_FACTOR):
    """
    Calculate the new Elo rating for a club based on a match result
    :param elo: Current Elo rating of the club
    :param score: Result of the match
    :param expected: Expected result of the match
    :param k: Modifiable k-factor
    :return: Updated Elo rating for the club
    """
    return elo + k * (score - expected)


def calculate_elo_ratings(matches, initial_elo=INITIAL_ELO, home_field_advantage=HOME_FIELD_ADVANTAGE, k=K_FACTOR,
                          print_error=True, season_reset=False, end_date=None, windows=WINDOWS,
                          window_weights=WINDOW_WEIGHTS):
    total_dif = 0
    baseline_dif = 0

    clubs, dates = get_clubs_and_matches(matches)
    elo_ratings = {club: initial_elo for club in clubs}
    elo_history = [{club: initial_elo for club in clubs} for _ in range(len(dates))]
    date_index = 0

    dates_played = {club: [] for club in clubs}

    results_comparison = [[], []]

    for match in matches:
        date, home_club, away_club, home_score, away_score, neutral = match
        if end_date is not None and end_date < date:
            break
        home_score = int(home_score)
        away_score = int(away_score)

        if season_reset:
            if date.year != dates[date_index].year:
                dates.insert(date_index + 1, dates[date_index] + timedelta(days=7))
                elo_history.insert(date_index + 1, {club: initial_elo for club in clubs})
                for club in clubs:
                    elo_history[date_index][club] = elo_ratings[club]

                elo_ratings = {club: initial_elo for club in clubs}
                dates_played = {club: [] for club in clubs}

                date_index += 1

        if date > dates[date_index]:
            # update the current elo ratings as we move to next date
            for club in clubs:
                elo_history[date_index][club] = elo_ratings[club]
            # and increment date index
            date_index += 1

        # if home_club not in elo_ratings:
        #     elo_ratings[home_club] = initial_elo
        # if away_club not in elo_ratings:
        #     elo_ratings[away_club] = initial_elo

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
        expected_home = expected_result(home_elo + (home_field_advantage * (not neutral)), away_elo)
        expected_away = expected_result(away_elo, home_elo + (home_field_advantage * (not neutral)))

        # home_k = int(k + (1000 * (1/(len(dates_played[home_club])+1))))
        # away_k = int(k + (1000 * (1/(len(dates_played[away_club])+1))))

        # home_k = max(int(k + ((20 - len(dates_played[home_club])) * 2)), k)
        # away_k = max(int(k + ((20 - len(dates_played[away_club])) * 2)), k)

        home_k = k
        away_k = k

        # Update Elo ratings
        updated_home_elo = update_elo(home_elo, home_result, expected_home, k=home_k)
        updated_away_elo = update_elo(away_elo, away_result, expected_away, k=away_k)

        # if date.year > 2023:
        #     updated_home_elo = update_elo(home_elo, 1 if random.random() < expected_home else 0,
        #                                   expected_home, k=home_k)
        #     updated_away_elo = update_elo(away_elo, 1 if random.random() < expected_away else 0,
        #                                   expected_away, k=away_k)

        # calculate error + baseline error
        dif = (home_result - expected_home) ** 2
        total_dif += dif
        baseline_dif += (home_result - 0.5) ** 2

        # store total results (?)
        results_comparison[0].append(expected_home)
        results_comparison[1].append(home_result)

        # print some interesting information!
        if abs(home_result - expected_home) > 0.98:
            print(date, f"({expected_home:.4f})", home_club, f"({home_elo:.2f})", home_score, "-", away_score,
                  away_club, f"({away_elo:.2f})")

        # store elo ratings
        elo_ratings[home_club] = updated_home_elo
        elo_ratings[away_club] = updated_away_elo

        # store dates played
        dates_played[home_club].append(date)
        dates_played[away_club].append(date)

    for club in clubs:
        elo_history[date_index][club] = elo_ratings[club]

    if print_error:
        print("total error:", total_dif)
        print("average error:", total_dif / len(matches))
        print("baseline average error", baseline_dif / len(matches))
        print("\n")

    return elo_ratings, elo_history, dates, results_comparison, total_dif/len(matches)


def get_clubs_and_matches(matches):
    """
    Extract and return each club and match date in a dataset of matches
    :param matches: list of matches, including (date, home_team, away_team, home_score, away_score, neutral)
    :return: tuple: (clubs, dates):
        - clubs: List of clubs in the dataset
        - dates: List of unique match dates in the dataset
    """
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


def plot_elo_ratings_over_time(arr, dates, clubs, club_metadata={}):
    # Ensure all dates are covered by filling in missing Elo ratings for non-match days
    full_elo_arr = []
    full_dates = []

    # Start from the first Elo array and date
    last_elo = arr[0].copy()
    last_date = dates[0]

    # Create a range of dates from the first to the last date in the dataset
    all_dates = [last_date]
    current_date = last_date

    # Generate all dates between the first and the last match date
    while current_date < dates[-1]:
        current_date += timedelta(days=1)
        all_dates.append(current_date)

    for current_date in all_dates:
        if current_date in dates:
            # On match days, use the corresponding Elo ratings
            date_index = dates.index(current_date)
            last_elo = arr[date_index]  # Update Elo ratings on match day
        # For non-match days, carry over the last Elo rating
        full_elo_arr.append(last_elo.copy())
        full_dates.append(current_date)

    # Plot the Elo ratings for each club over time
    # clubs = ["Louisville", "Gotham"]
    for club in clubs:
        if club in full_elo_arr[0]:
            elo_over_time = [elo_ratings[club] for elo_ratings in full_elo_arr]
            club_dates = []
            club_elos = []
            for i in range(len(full_dates)):
                if club in club_metadata:
                    if club_metadata[club][0] < full_dates[i] < club_metadata[club][1]:
                        club_dates.append(full_dates[i])
                        club_elos.append(full_elo_arr[i][club])
            if club in club_metadata:
                if len(club_metadata[club]) > 2:
                    plt.plot(club_dates, club_elos, club_metadata[club][2], label=club)
                else:
                    plt.plot(club_dates, club_elos, label=club)
            else:
                plt.plot(full_dates, elo_over_time, label=club)
        else:
            print("club " + club + " does not exist")


    # Plot settings
    plt.xlabel('Date')
    plt.ylabel('Elo Rating')
    plt.title('Elo Ratings Over Time')
    plt.legend()
    plt.xticks(rotation=45)  # Rotate the x-axis labels if needed
    plt.tight_layout()
    plt.legend(fontsize='small')
    plt.show()


if __name__ == "__main__":
    a = 1800
    b = 1000
    HOME_FIELD_ADVANTAGE = 0
    exp_a = expected_result(a + HOME_FIELD_ADVANTAGE, b)
    exp_b = expected_result(b, a + HOME_FIELD_ADVANTAGE)
    print(exp_a)
    print(update_elo(a, 0.5, exp_a))
    print(update_elo(b, 0.5, exp_b))
