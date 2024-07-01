import math
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

INITIAL_ELO = 1000
K_FACTOR = 50  # The K-factor determines the maximum possible change in rating.
HOME_FIELD_ADVANTAGE = 60  # Elo points added to the home team's rating for home advantage - 60 by experiment


def expected_result(elo_a, elo_b):
    return 1 / (1 + math.pow(10, (elo_b - elo_a) / 400))


def update_elo(elo, score, expected):
    return elo + K_FACTOR * (score - expected)


def calculate_elo_ratings(matches):
    total_dif = 0

    elo_ratings = {}
    elo_history = defaultdict(list)
    cur_date = datetime.strptime(matches[0][0], "%Y-%m-%d")
    all_dates = sorted(set([datetime.strptime(match[0], "%Y-%m-%d") for match in matches]))

    for match in matches:
        date, home_team, away_team, home_score, away_score = match
        match_date = datetime.strptime(date, "%Y-%m-%d")
        cur_date = max(cur_date, match_date)

