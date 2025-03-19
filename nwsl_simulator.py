import random
from datetime import datetime
from collections import defaultdict

import elo
import reader
from table import LeagueTable


def calculate_probs(expected_result):
    draw = -1.008241359 * ((expected_result ** 2) - expected_result)
    win = expected_result - (draw / 2)
    loss = 1 - win - draw
    return win, draw, loss


def run_simulation(num_simulations=10000, hfa=45, k=32, sr=0.5511):
    matches = reader.read_matches_obj("nwsl_matches.txt")
    today = datetime(2025, 3, 13)
    # today = datetime.today()
    completed_matches = [match for match in matches if match.date <= today]
    incomplete_matches = [match for match in matches if match.date > today]

    ranking_counts = defaultdict(lambda: defaultdict(int))

    for sim_index in range(num_simulations):
        elo_ratings, _, _, _, _ = elo.calculate_elo_ratings(completed_matches, print_error=False,
                                                            home_field_advantage=hfa, k=k,
                                                            season_reset=sr,
                                                            end_date=datetime(2028, 10, 22),
                                                            reset_date=datetime(1, 1, 1))
        nwsl_table = LeagueTable()

        for match in completed_matches:
            if match.date.year == 2025 and match.regular_season:
                nwsl_table.record_match(match.home_club, match.away_club, match.home_score, match.away_score)

        # nwsl_table.deduct_points("Angel City", 3)

        for match in incomplete_matches:
            random_number = random.random()
            expected_result = elo.expected_result(elo_ratings[match.home_club] + hfa, elo_ratings[match.away_club])
            win, draw, loss = calculate_probs(expected_result)

            if win > random_number:
                nwsl_table.record_match(match.home_club, match.away_club, 2, 0)
                home_result = 1
                away_result = 0
            elif win + draw > random_number:
                nwsl_table.record_match(match.home_club, match.away_club, 1, 1)
                home_result = 0
                away_result = 1
            else:
                nwsl_table.record_match(match.home_club, match.away_club, 0, 2)
                home_result = 0.5
                away_result = 0.5

            expected_home = elo.expected_result(elo_ratings[match.home_club] + (hfa * (not match.neutral)),
                                                elo_ratings[match.away_club])
            expected_away = elo.expected_result(elo_ratings[match.away_club],
                                                elo_ratings[match.home_club] + (hfa * (not match.neutral)))

            updated_home_elo = elo.update_elo(elo_ratings[match.home_club], home_result, expected_home, k=k)
            updated_away_elo = elo.update_elo(elo_ratings[match.away_club], away_result, expected_away, k=k)

            elo_ratings[match.home_club] = updated_home_elo
            elo_ratings[match.away_club] = updated_away_elo

        sorted_clubs = sorted(nwsl_table.clubs.values(), key=lambda x: (x.points, x.goal_difference(), x.goals_scored),
                              reverse=True)
        for rank, club in enumerate(sorted_clubs, start=1):
            ranking_counts[club.name][rank] += 1

    print("Final Standings Probabilities:")
    for club, ranks in ranking_counts.items():
        first_place_prob = (ranks.get(1, 0) / num_simulations) * 100
        top_4_prob = (sum(ranks.get(r, 0) for r in range(1, 5)) / num_simulations) * 100
        top_8_prob = (sum(ranks.get(r, 0) for r in range(1, 9)) / num_simulations) * 100

        print(f"{club}:")
        print(f"  1st: {first_place_prob:.2f}%")
        print(f"  Top 4: {top_4_prob:.2f}%")
        print(f"  Top 8: {top_8_prob:.2f}%")


if __name__ == "__main__":
    run_simulation()
