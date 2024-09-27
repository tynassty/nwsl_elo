import math
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
from datetime import timedelta
import reader
import numpy as np

INITIAL_ELO = 1000
K_FACTOR = 40  # The K-factor determines the (NORMAL) maximum possible change in rating.
HOME_FIELD_ADVANTAGE = 60  # Elo points added to the home team's rating for home advantage - 60 by experiment
WINDOW = 100  # window of days to check number of matches played (for adjusting k factors)

FIRST_DATE = datetime(2013, 4, 13)
FINAL_DATE = datetime.today()
CLUB_METADATA = {
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


def expected_result(elo_a, elo_b):
    return 1 / (1 + math.pow(10, (elo_b - elo_a) / 400))


def update_elo(elo, score, expected, k=K_FACTOR):
    return elo + k * (score - expected)


def calculate_elo_ratings(matches):
    total_dif = 0
    baseline_dif = 0

    clubs, dates = get_clubs_and_matches(matches)
    elo_ratings = {club: INITIAL_ELO for club in clubs}
    arr = [{club: INITIAL_ELO for club in clubs} for _ in range(len(dates))]
    date_index = 0

    dates_played = {club: [] for club in clubs}

    total_results = [[], []]

    for match in matches:
        date, home_club, away_club, home_score, away_score = match
        if date > dates[date_index]:
            # update the current elo ratings as we move to next date
            for club in clubs:
                arr[date_index][club] = elo_ratings[club]
            # and increment date index
            date_index += 1

        # if home_club not in elo_ratings:
        #     elo_ratings[home_club] = INITIAL_ELO
        # if away_club not in elo_ratings:
        #     elo_ratings[away_club] = INITIAL_ELO

        home_elo = elo_ratings[home_club]
        away_elo = elo_ratings[away_club]

        dates_played[home_club].append(date)
        dates_played[away_club].append(date)

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
        baseline_dif += abs(home_result - 0.5)

        total_results[0].append(expected_home)
        total_results[1].append(home_result)

        # if expected_home > 0.9:
        #     print(expected_home, home_club, "(", home_elo, ")", home_score, "-", away_score, away_club, "(", away_elo, ")", date)

        # store elo ratings
        elo_ratings[home_club] = new_home_elo
        elo_ratings[away_club] = new_away_elo

    for club in clubs:
        arr[date_index][club] = elo_ratings[club]

    print("total error:", total_dif)
    print("average error:", total_dif / len(matches))
    print("baseline average error", baseline_dif / len(matches))

    print("\n")

    return elo_ratings, arr, dates, total_results


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


def plot_elo_ratings_over_time(arr, dates, clubs):
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

        elo_over_time = [elo_ratings[club] for elo_ratings in full_elo_arr]
        club_dates = []
        club_elos = []
        for i in range(len(full_dates)):
            if CLUB_METADATA[club][0] < full_dates[i] < CLUB_METADATA[club][1]:
                club_dates.append(full_dates[i])
                club_elos.append(full_elo_arr[i][club])
        if len(CLUB_METADATA[club]) > 2:
            plt.step(club_dates, club_elos, CLUB_METADATA[club][2], label=club)
        else:
            plt.step(club_dates, club_elos, label=club)

    # Plot settings
    plt.xlabel('Date')
    plt.ylabel('Elo Rating')
    plt.title('Elo Ratings Over Time (Including Non-Match Days)')
    plt.legend()
    plt.xticks(rotation=45)  # Rotate the x-axis labels if needed
    plt.tight_layout()
    plt.show()


# Example usage:

matches = reader.read_matches("matches.txt")
elo_ratings, arr, dates, total_results = calculate_elo_ratings(matches)
# for elo_rating in elo_ratings:
#     print(elo_rating, elo_ratings[elo_rating])

number = 44.5

clubs, _ = get_clubs_and_matches(matches)
plot_elo_ratings_over_time(arr, dates, clubs)
