import random
from datetime import datetime
from collections import defaultdict
import numpy as np

import elo
import reader
from table import LeagueTable


def calculate_probs(expected_result):
    draw = -1.008241359 * ((expected_result ** 2) - expected_result)
    win = expected_result - (draw / 2)
    loss = 1 - win - draw
    return win, draw, loss


def simulate_match_score(expected_result):
    expected_gd = 5.51 * expected_result - 2.755  # Expected goal difference

    # Adjust Poisson lambda for each team based on expected goal difference
    base_lambda = 1.4
    home_lambda = max(base_lambda + (expected_gd / 2), 0)  # Ensure lambda is positive
    away_lambda = max(base_lambda - (expected_gd / 2), 0)

    # Sample goals from Poisson with adjusted lambda
    goals_a = np.random.poisson(home_lambda)
    goals_b = np.random.poisson(away_lambda)

    return goals_a, goals_b


def simulate_playoffs(top8, elo_ratings, hfa, k, playoff_round_counts, playoff_seed_order):
    seed_list = top8[:]  # Initial seeding order

    # Record all 8 teams making the playoffs
    for team in seed_list:
        playoff_round_counts[team]["Quarterfinals"] += 1

    round_number = 0
    round_names = ["Semifinals", "Finals", "Champions"]

    while len(seed_list) > 1:
        t_hfa = hfa if round_number == 0 else 0
        next_round = []

        for i in range(len(seed_list) // 2):
            team1 = seed_list[i]
            team2 = seed_list[-1 - i]

            # Ensure the better seed (lower rank number) is team1
            if playoff_seed_order[team1] > playoff_seed_order[team2]:
                team1, team2 = team2, team1

            win_prob = elo.expected_result(elo_ratings[team1] + t_hfa, elo_ratings[team2])
            winner = team1 if random.random() <= win_prob else team2

            # Update Elo ratings
            elo_ratings[team1] = elo.update_elo(elo_ratings[team1], team1 == winner, win_prob, k=k)
            elo_ratings[team2] = elo.update_elo(elo_ratings[team2], team2 == winner, 1 - win_prob, k=k)

            # Record advancement
            playoff_round_counts[winner][round_names[round_number]] += 1

            next_round.append(winner)

        seed_list = next_round
        round_number += 1

    return seed_list[0]  # The champion


def run_simulation(num_simulations=10000, hfa=45, k=32, sr=0.5511, today=datetime.today()):
    matches = reader.read_matches_obj("nwsl_matches.txt")
    completed_matches, incomplete_matches = [], []
    for match in matches:
        (completed_matches if match.date <= today and match.is_complete() else incomplete_matches).append(match)

    regular_season_ranking_counts = defaultdict(lambda: defaultdict(int))
    playoff_round_counts = defaultdict(lambda: defaultdict(int))
    total_ranks = defaultdict(int)

    # Precompute Elo ratings from completed matches once
    base_elo_ratings, _, _, _, _ = elo.calculate_elo_ratings(
        completed_matches,
        print_error=False,
        home_field_advantage=hfa,
        k=k,
        season_reset=sr,
        end_date=datetime(2028, 10, 22),
        reset_date=datetime(1, 1, 1)
    )

    for sim_index in range(num_simulations):
        # Copy precomputed ratings for each simulation
        elo_ratings = base_elo_ratings.copy()

        nwsl_table = LeagueTable()

        for match in completed_matches:
            if match.date.year == 2025 and match.regular_season:
                nwsl_table.record_match(match.home_club, match.away_club, match.home_score, match.away_score)

        for match in incomplete_matches:
            random_number = random.random()
            expected_result = elo.expected_result(elo_ratings[match.home_club] + hfa, elo_ratings[match.away_club])
            # win, draw, loss = calculate_probs(expected_result)

            # if win > random_number:
            #     nwsl_table.record_match(match.home_club, match.away_club, 2, 0)
            #     home_result, away_result = 1, 0
            # elif win + draw > random_number:
            #     nwsl_table.record_match(match.home_club, match.away_club, 1, 1)
            #     home_result, away_result = 0.5, 0.5
            # else:
            #     nwsl_table.record_match(match.home_club, match.away_club, 0, 2)
            #     home_result, away_result = 0, 1

            home_score, away_score = simulate_match_score(expected_result)
            nwsl_table.record_match(match.home_club, match.away_club, home_score, away_score)
            if home_score > away_score:
                home_result, away_result = 1, 0
            elif home_score == away_score:
                home_result, away_result = 0.5, 0.5
            else:
                home_result, away_result = 0, 1

            expected_home = elo.expected_result(
                elo_ratings[match.home_club] + (hfa * (not match.neutral)),
                elo_ratings[match.away_club]
            )
            expected_away = elo.expected_result(
                elo_ratings[match.away_club],
                elo_ratings[match.home_club] + (hfa * (not match.neutral))
            )

            elo_ratings[match.home_club] = elo.update_elo(elo_ratings[match.home_club], home_result, expected_home, k=k)
            elo_ratings[match.away_club] = elo.update_elo(elo_ratings[match.away_club], away_result, expected_away, k=k)

        sorted_clubs = sorted(
            nwsl_table.clubs.values(),
            key=lambda x: (x.points, x.goal_difference(), x.goals_scored),
            reverse=True
        )

        for rank, club in enumerate(sorted_clubs, start=1):
            regular_season_ranking_counts[club.name][rank] += 1
            total_ranks[club.name] += rank

        if len(sorted_clubs) < 8:
            continue
        top8 = [club.name for club in sorted_clubs[:8]]
        playoff_seed_order = {team: rank for rank, team in enumerate(top8, start=1)}

        # PRINT CHECK
        print("STANDINGS SIM #", sim_index)
        nwsl_table.standings()
        print()

        # Simulate playoffs
        elo_ratings_copy = elo_ratings.copy()
        simulate_playoffs(top8, elo_ratings_copy, hfa, k, playoff_round_counts, playoff_seed_order)

    # Print Regular Season Stats
    print("Regular Season Final Standings Probabilities:")
    for club, ranks in regular_season_ranking_counts.items():
        first_place_prob = (ranks.get(1, 0) / num_simulations) * 100
        top4_prob = (sum(ranks.get(r, 0) for r in range(1, 5)) / num_simulations) * 100
        top8_prob = (sum(ranks.get(r, 0) for r in range(1, 9)) / num_simulations) * 100
        avg_rank = total_ranks[club] / num_simulations if club in total_ranks else None

        print(f"{club}:")
        print(f"  1st: {first_place_prob:.2f}%")
        print(f"  Top 4: {top4_prob:.2f}%")
        print(f"  Top 8: {top8_prob:.2f}%")
        print(f"  Avg Rank: {avg_rank:.2f}")

    # Print Playoff Stats
    print("\nPlayoff Advancement Probabilities:")
    for club, rounds in playoff_round_counts.items():
        qf_prob = (rounds["Quarterfinals"] / num_simulations) * 100
        sf_prob = (rounds["Semifinals"] / num_simulations) * 100
        f_prob = (rounds["Finals"] / num_simulations) * 100
        champ_prob = (rounds["Champions"] / num_simulations) * 100
        print(f"{club}:")
        print(f"  Playoffs: {qf_prob:.2f}%")
        print(f"  Semifinals: {sf_prob:.2f}%")
        print(f"  Finals: {f_prob:.2f}%")
        print(f"  Champions: {champ_prob:.2f}%")

    # for i in range(10):
    #     print("-----------------------")

    print("Club,Shield,HomeQF,Playoffs,AvgRank")
    for club in sorted(regular_season_ranking_counts.keys()):
        shield_prob = regular_season_ranking_counts[club].get(1, 0) / num_simulations
        home_qf_prob = sum(regular_season_ranking_counts[club].get(r, 0) for r in range(1, 5)) / num_simulations
        playoffs_prob = sum(regular_season_ranking_counts[club].get(r, 0) for r in range(1, 9)) / num_simulations
        avg_rank = total_ranks[club] / num_simulations if club in total_ranks else None
        print(f"{club},{shield_prob:.4f},{home_qf_prob:.4f},{playoffs_prob:.4f},{avg_rank:.4f}")


if __name__ == "__main__":
    # run_simulation(today=datetime.today())
    run_simulation(num_simulations=1000)


