import math
import random
from Match import Match
from matplotlib import pyplot as plt, gridspec
from collections import defaultdict
from datetime import datetime
from datetime import timedelta
from typing import List

import ncaaf_test
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


def calculate_elo_ratings(matches: List[Match], initial_elo=INITIAL_ELO, home_field_advantage=HOME_FIELD_ADVANTAGE,
                          k=K_FACTOR,
                          print_error=True, season_reset=False, reset_date=datetime(1, 1, 1), end_date=None,
                          windows=WINDOWS, window_weights=WINDOW_WEIGHTS, decay_target=None):
    """
    Calculate the Elo ratings for a list of matches.

    :param matches: List of match data. Each match is a tuple consisting of
                    (date, home_team, away_team, home_score, away_score, neutral), where:
                    - date: datetime object representing when the match took place.
                    - home_team: Name of the home club.
                    - away_team: Name of the away club.
                    - home_score: Final score of the home club.
                    - away_score: Final score of the away club.
                    - neutral: Boolean value indicating whether the match was played at a neutral venue.
    :param initial_elo: The initial Elo rating for all clubs at the start (default=1000).
    :param home_field_advantage: The amount of Elo points added to the home team due to home advantage
                                 (default=72 points).
    :param k: The K-factor, which determines the maximum change in Elo after a match (default=52).
    :param print_error: Boolean indicating whether to print error statistics (default=True).
    :param season_reset: Allows for resetting the Elo ratings at the start of a new season. If `True`, ratings reset to
                         `initial_elo` at the start of a new year. If a float value between 0 and 1 is given, the
                         ratings will proportionally reset, blending `initial_elo` with the club's previous Elo
                         (default=False).
    :param reset_date: date to reset on if season reset
    :param end_date: Optional datetime value; matches after this date will be excluded (default=None).
    :param windows: A list of time periods (in days) for weighted Elo calculations. Allows tracking club performance
                    over different windows, e.g., last 10 days, last month, last year (default=[10, 31, 365]).
    :param window_weights: Weights associated with each window in `windows`, used to adjust Elo updates based on
                           recent form. By default, weights are zeroed out (default=[0, 0, 0]).
    :return: A tuple of results:
             - elo_ratings: Final Elo ratings for all clubs after processing the matches.
             - elo_history: Elo ratings for all clubs at each point in time (each match date).
             - dates: List of unique match dates.
             - results_comparison: List of two sublists comparing expected and actual results:
                                   1. Expected results for the home team.
                                   2. Actual results for the home team.
             - brier_score: The average mean square error between expected and actual results over all matches.
    """
    if decay_target is None:
        decay_target = initial_elo
    total_dif = 0
    baseline_dif = 0

    clubs, dates = get_clubs_and_matches(matches)
    elo_ratings = {club: initial_elo for club in clubs}

    elo_history = [{club: initial_elo for club in clubs} for _ in range(len(dates))]
    date_index = 0

    dates_played = {club: [] for club in clubs}

    results_comparison = [[], []]

    reset_date = datetime(matches[0].date.year + 1, reset_date.month, reset_date.day)

    for match in matches:
        # j;dahfadjkljdkllkadjsfkla;klf
        # lfsf;d;kdjv;af;lkjd;lkfjk;
        # dkqlfkjas;lfkja;ld
        # date, home_club, away_club, home_score, away_score, neutral, regular_season = match

        if end_date is not None and end_date < match.date:
            break

        home_score = int(match.home_score)
        away_score = int(match.away_score)

        if season_reset:
            # if date.year != dates[date_index].year:
            if match.date > reset_date:
                reset_date = datetime(reset_date.year + 1, reset_date.month, reset_date.day)
                dates.insert(date_index + 1, dates[date_index] + timedelta(days=28))
                elo_history.insert(date_index + 1, {club: initial_elo for club in clubs})
                for club in clubs:
                    elo_history[date_index][club] = elo_ratings[club]

                elo_ratings = {club: (decay_target * season_reset) + (elo_ratings[club] * (1 - season_reset)) for club
                               in clubs}
                dates_played = {club: [] for club in clubs}

                date_index += 1

        if match.date > dates[date_index]:
            # update the current elo ratings as we move to next date
            for club in clubs:
                elo_history[date_index][club] = elo_ratings[club]
            # and increment date index
            date_index += 1

        # if home_club not in elo_ratings:
        #     elo_ratings[home_club] = initial_elo
        # if away_club not in elo_ratings:
        #     elo_ratings[away_club] = initial_elo

        home_elo = elo_ratings[match.home_club]
        away_elo = elo_ratings[match.away_club]

        if match.home_score > match.away_score:
            home_result = 1
            away_result = 0
        elif match.home_score < match.away_score:
            home_result = 0
            away_result = 1
        else:
            home_result = 0.5
            away_result = 0.5

        # calc expected results
        expected_home = expected_result(home_elo + (home_field_advantage * (not match.neutral)), away_elo)
        expected_away = expected_result(away_elo, home_elo + (home_field_advantage * (not match.neutral)))

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
        # todays_clubs = [match.home_club, match.away_club]
        # if abs(home_result - expected_home) > 0.95 and all(club in ncaaf_test.SEC for club in todays_clubs):
        # if abs(home_result - expected_home) > 0.95:
        #     print(match.date, f"({expected_home:.4f})", match.home_club, f"({home_elo:.2f})", home_score, "-",
        #           away_score, match.away_club, f"({away_elo:.2f})")

        # store elo ratings
        elo_ratings[match.home_club] = updated_home_elo
        elo_ratings[match.away_club] = updated_away_elo

        # store dates played
        dates_played[match.home_club].append(match.date)
        dates_played[match.away_club].append(match.date)

    for club in clubs:
        elo_history[date_index][club] = elo_ratings[club]

    brier_score = total_dif / len(matches)

    if print_error:
        print("Brier score:", brier_score)
        print("baseline Brier score", baseline_dif / len(matches))
        print("\n")

    return elo_ratings, elo_history, dates, results_comparison, brier_score


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
        if match.date not in dates:
            dates.append(match.date)
        if match.home_club not in clubs:
            clubs.append(match.home_club)
        if match.away_club not in clubs:
            clubs.append(match.away_club)
    return clubs, dates


def plot_elo_ratings_over_time(arr, dates, clubs, club_metadata=None, block=True):
    if club_metadata is None:
        club_metadata = {}

    # create a new figure
    plt.figure()

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

    # Build the full Elo array for every date
    for current_date in all_dates:
        if current_date in dates:
            # On match days, update Elo ratings
            date_index = dates.index(current_date)
            last_elo = arr[date_index]
        # Carry over the last Elo rating for non-match days
        full_elo_arr.append(last_elo.copy())
        full_dates.append(current_date)

    # Plot the Elo ratings for each club over time
    for club in clubs:
        if club in full_elo_arr[0]:
            # Elo ratings for the current club over time
            elo_over_time = [elo_ratings[club] for elo_ratings in full_elo_arr]

            # Filter based on club metadata if available
            if club in club_metadata:
                club_dates = []
                club_elos = []
                start_date, end_date = club_metadata[club][:2]
                for i, date in enumerate(full_dates):
                    if start_date < date < end_date:
                        club_dates.append(date)
                        club_elos.append(full_elo_arr[i][club])

                # Plot with custom styles if metadata includes them
                lw = 1.6
                if len(club_metadata[club]) == 3:
                    plt.plot(club_dates, club_elos, club_metadata[club][2], label=club, linewidth=lw)
                elif len(club_metadata[club]) == 4:
                    grid = gridspec.GridSpec(1, 1)
                    plt.plot(club_dates, club_elos, club_metadata[club][2], label=club, dashes=[6, 2], linewidth=lw,
                             gapcolor=club_metadata[club][3])
                else:
                    plt.plot(club_dates, club_elos, label=club, linewidth=lw)
            else:
                # Plot without filtering if no metadata
                plt.plot(full_dates, elo_over_time, label=club)
        else:
            print(f"Club {club} does not exist")

    # Plot settings
    plt.xlabel('Date')
    plt.ylabel('Elo Rating')
    plt.title('Elo Ratings Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend(fontsize='small')
    plt.show(block=block)


if __name__ == "__main__":
    a = 2000
    b = 1000
    HOME_FIELD_ADVANTAGE = 0
    exp_a = expected_result(a + HOME_FIELD_ADVANTAGE, b)
    exp_b = expected_result(b, a + HOME_FIELD_ADVANTAGE)
    print(exp_a)
    print(update_elo(a, 0.5, exp_a))
    print(update_elo(b, 0.5, exp_b))
