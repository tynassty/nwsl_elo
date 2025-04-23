import random
from datetime import datetime
from collections import defaultdict
import multiprocessing
import json
import numpy as np

import nwsl_simulator
import elo
import reader
from table import LeagueTable


# Helper to create a defaultdict(int) for nested dictionaries
def dd_int():
    return defaultdict(int)


# Helper to recursively convert defaultdicts to regular dicts.
def convert_defaultdict(d):
    if isinstance(d, defaultdict):
        return {k: convert_defaultdict(v) for k, v in d.items()}
    return d


def simulate_playoffs(top8, elo_ratings, hfa, k, playoff_round_counts, playoff_seed_order):
    seed_list = top8[:]  # Initial seeding order
    # Record all 8 teams making the playoffs (Quarterfinals)
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
            # Ensure the better seed is team1
            if playoff_seed_order[team1] > playoff_seed_order[team2]:
                team1, team2 = team2, team1
            win_prob = elo.expected_result(elo_ratings[team1] + t_hfa, elo_ratings[team2])
            winner = team1 if random.random() <= win_prob else team2

            # Update Elo ratings
            elo_ratings[team1] = elo.update_elo(elo_ratings[team1], team1 == winner, win_prob, k=k)
            elo_ratings[team2] = elo.update_elo(elo_ratings[team2], team2 == winner, 1 - win_prob, k=k)
            playoff_round_counts[winner][round_names[round_number]] += 1
            next_round.append(winner)
        seed_list = next_round
        round_number += 1
    return seed_list[0]  # The champion


def simulate_one(base_elo_ratings, completed_matches, incomplete_matches, hfa, k, sr):
    """
    Run one simulation iteration.
    Returns:
      regular_season_counts: dict {club: {rank: count}}
      playoff_counts: dict {club: {round: count}}
      total_ranks: dict {club: total_rank_sum}
    """
    # Copy the precomputed Elo ratings for this simulation
    elo_ratings = base_elo_ratings.copy()
    nwsl_table = LeagueTable()
    # Use top-level functions to initialize defaultdicts instead of lambdas.
    regular_season_counts = defaultdict(dd_int)
    total_ranks = defaultdict(int)
    playoff_counts = defaultdict(dd_int)

    # Process completed matches (for 2025 regular season)
    for match in completed_matches:
        # Assume match.regular_season is a boolean
        if match.date.year == 2025 and match.regular_season:
            nwsl_table.record_match(match.home_club, match.away_club, match.home_score, match.away_score)

    # Process incomplete matches by simulating outcomes
    for match in incomplete_matches:
        random_number = random.random()
        expected_result = elo.expected_result(elo_ratings[match.home_club] + hfa, elo_ratings[match.away_club])
        # win, draw, loss = nwsl_simulator.calculate_probs(expected_result)

        # if win > random_number:
        #     nwsl_table.record_match(match.home_club, match.away_club, 2, 0)
        #     home_result, away_result = 1, 0
        # elif win + draw > random_number:
        #     nwsl_table.record_match(match.home_club, match.away_club, 1, 1)
        #     home_result, away_result = 0.5, 0.5
        # else:
        #     nwsl_table.record_match(match.home_club, match.away_club, 0, 2)
        #     home_result, away_result = 0, 1

        home_score, away_score = nwsl_simulator.simulate_match_score(expected_result)
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

    # Calculate regular season standings
    sorted_clubs = sorted(
        nwsl_table.clubs.values(),
        key=lambda x: (x.points, x.goal_difference(), x.goals_scored),
        reverse=True
    )
    for rank, club in enumerate(sorted_clubs, start=1):
        regular_season_counts[club.name][rank] += 1
        total_ranks[club.name] += rank

    # If at least 8 clubs qualify, simulate playoffs
    if len(sorted_clubs) >= 8:
        top8 = [club.name for club in sorted_clubs[:8]]
        playoff_seed_order = {team: rank for rank, team in enumerate(top8, start=1)}
        # simulate_playoffs(top8, elo_ratings.copy(), hfa, k, playoff_counts, playoff_seed_order)

    # Convert nested defaultdicts to dicts for pickling
    return (convert_defaultdict(regular_season_counts), convert_defaultdict(playoff_counts), dict(total_ranks))


def aggregate_results(results, num_simulations):
    """
    Combine the dictionaries from multiple simulation iterations.
    """
    agg_regular = defaultdict(dd_int)
    agg_playoffs = defaultdict(dd_int)
    agg_total_ranks = defaultdict(int)

    for reg, play, tot in results:
        for club, ranks in reg.items():
            for rank, count in ranks.items():
                agg_regular[club][rank] += count
        for club, rounds in play.items():
            for round_name, count in rounds.items():
                agg_playoffs[club][round_name] += count
        for club, rank_sum in tot.items():
            agg_total_ranks[club] += rank_sum

    # Compute average rank per club over simulations
    avg_ranks = {club: agg_total_ranks[club] / num_simulations for club in agg_total_ranks}
    return agg_regular, agg_playoffs, avg_ranks


def run_simulation(num_simulations=10000, hfa=45, k=32, sr=0.5511, today=datetime.today()):
    matches = reader.read_matches_obj("nwsl_matches.txt")
    completed_matches, incomplete_matches = [], []
    for match in matches:
        (completed_matches if match.date <= today and match.is_complete() else incomplete_matches).append(match)

    # Precompute the base Elo ratings from completed matches
    base_elo_ratings, _, _, _, _ = elo.calculate_elo_ratings(
        completed_matches,
        print_error=False,
        home_field_advantage=hfa,
        k=k,
        season_reset=sr,
        end_date=datetime(2028, 10, 22),
        reset_date=datetime(1, 1, 1)
    )

    # Prepare arguments for each simulation iteration
    sim_args = (base_elo_ratings, completed_matches, incomplete_matches, hfa, k, sr)

    # Run simulations in parallel
    with multiprocessing.Pool() as pool:
        results = pool.starmap(simulate_one, [sim_args for _ in range(num_simulations)])

    # Aggregate results across all simulations
    reg_counts, playoff_counts, avg_ranks = aggregate_results(results, num_simulations)

    # Format output (CSV style) for easy copying into your spreadsheet.
    print("Club,Shield,HomeQF,Playoffs,AvgRank")
    clubs = sorted(reg_counts.keys())
    for club in clubs:
        # Shield: chance to finish first
        shield_prob = reg_counts[club].get(1, 0) / num_simulations
        # HomeQF: chance to finish in top 4
        home_qf_prob = sum(reg_counts[club].get(r, 0) for r in range(1, 5)) / num_simulations
        # Playoffs: chance to finish in top 8
        playoffs_prob = home_qf_prob + sum(reg_counts[club].get(r, 0) for r in range(5, 9)) / num_simulations
        avg_rank = avg_ranks.get(club, 0)
        print(f"{club},{shield_prob:.5f},{home_qf_prob:.5f},{playoffs_prob:.5f},{avg_rank:.5f}")

    # Optionally, print playoff advancement probabilities.
    # print("\nPlayoff Advancement Probabilities:")
    # for club in sorted(playoff_counts.keys()):
    #     qf_prob = playoff_counts[club].get("Quarterfinals", 0) / num_simulations
    #     sf_prob = playoff_counts[club].get("Semifinals", 0) / num_simulations
    #     f_prob = playoff_counts[club].get("Finals", 0) / num_simulations
    #     champ_prob = playoff_counts[club].get("Champions", 0) / num_simulations
    #     print(f"{club} - QF: {qf_prob:.4f}, SF: {sf_prob:.4f}, F: {f_prob:.4f}, Champ: {champ_prob:.4f}")


if __name__ == "__main__":
    run_simulation(today=datetime.today(), num_simulations=100000)
    # run_simulation(today=datetime(2025, 4, 22), num_simulations=100000)

    # for i in range(15, 18):
    #     print(i)
    #     run_simulation(today=datetime(2025, 4, i), num_simulations=100000)

    # run_simulation(today=datetime(2025, 3, 18), num_simulations=10)
