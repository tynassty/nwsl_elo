import datetime
import random

import numpy as np

import elo
import reader


def average_ranking(club):
    # Create an array of positions starting from 1 to the length of syracuse
    positions = np.arange(1, len(club) + 1)

    # Calculate the weighted sum of rankings
    weighted_sum = np.dot(positions, club)

    # Calculate the total number of rankings
    total_rankings = np.sum(club)

    # Compute the average ranking
    if total_rankings == 0:
        return None  # Avoid division by zero if no rankings exist
    else:
        return weighted_sum / total_rankings


# matches = reader.read_matches("ncaaf.txt")
matches = reader.read_matches_2("ncaaf2.txt")
# matches = [match for match in matches if match[0] < datetime.datetime(2024, 9, 26)]

clubs, _ = elo.get_clubs_and_matches(matches)
# clubs = ["Florida State", "Louisville", "North Carolina State", "Georgia Tech", "Virginia Tech", "North Carolina",
#          "Clemson", "Duke", "Miami (FL)", "Boston College", "Syracuse", "Virginia", "Pittsburgh", "Wake Forest",
#          "Southern Methodist", "California", "Stanford"]

rank_dict = {club: [0 for _ in range(len(clubs))] for club in clubs}

for i in range(100):
    random.shuffle(clubs)

    # today = 0
    today = 0

    for match in matches:
        p = False
        date, home_club, away_club, home_score, away_score, neutral = match
        if today != date:
            today = date

        if home_club not in clubs:
            continue
        elif away_club not in clubs:
            continue

        home_index = clubs.index(home_club)
        away_index = clubs.index(away_club)
        home_score = int(home_score)
        away_score = int(away_score)

        if home_score > away_score:
            if home_index > away_index:
                clubs[home_index], clubs[away_index] = clubs[away_index], clubs[home_index]
        elif away_score > home_score:
            if away_index > home_index:
                clubs[home_index], clubs[away_index] = clubs[away_index], clubs[home_index]

        # if date != today:
        #     today = date
        #     print(today, clubs)

        # print(date, clubs)

    for j in range(len(clubs)):
        rank_dict[clubs[j]][j] += 1

    print(clubs)
    # print(i)

avg_rank_dict = {club: 0 for club in rank_dict}

for key in rank_dict:
    avg_rank_dict[key] = average_ranking(rank_dict[key])

# print(avg_rank_dict)
sorted_rankings = sorted(avg_rank_dict, key=avg_rank_dict.get)
print("FINAL RANKINGS:")
print(sorted_rankings)

for i in range(len(sorted_rankings)):
    print(i+1, sorted_rankings[i], avg_rank_dict[sorted_rankings[i]], "(" + str(rank_dict[sorted_rankings[i]][0]) + ")")


