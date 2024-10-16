import datetime

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


if __name__ == "__main__":
    matches = reader.read_matches("ncaaf.txt")
    recent_matches = [match for match in matches if match[0] > datetime.datetime(2023, 10, 3)]
    # recent_matches = matches
    clubs, _ = elo.get_clubs_and_matches(recent_matches)
    rank_dict = {club: [0 for _ in range(len(clubs))] for club in clubs}
    for i in range(1, 201, 2):
        elo_ratings, _, _, _, _ = elo.calculate_elo_ratings(matches, initial_elo=1000, home_field_advantage=0,
                                                            k=i, print_error=False)
        sorted_elos = sorted(elo_ratings, key=elo_ratings.get)
        sorted_elos = [elo for elo in sorted_elos if elo in clubs]
        sorted_elos.reverse()
        print(i, sorted_elos)

        for j in range(len(sorted_elos)):
            rank_dict[sorted_elos[j]][j] += 1

    avg_rank_dict = {club: 0 for club in rank_dict}

    for key in rank_dict:
        avg_rank_dict[key] = average_ranking(rank_dict[key])

    sorted_rankings = sorted(avg_rank_dict, key=avg_rank_dict.get)
    # print("FINAL RANKINGS:")
    # print(sorted_rankings)

    for i in range(len(sorted_rankings)):
        print(i + 1, sorted_rankings[i], avg_rank_dict[sorted_rankings[i]],
              "(" + str(rank_dict[sorted_rankings[i]][0]) + ")")


