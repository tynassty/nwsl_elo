import random
import elo
import ncaaf_test
import reader
from datetime import datetime
import math


def next_power_of_two(a):
    n = 0
    while 2 ** n < a:
        n += 1
    return 2 ** n


def extend_to_next_power_of_two(initial_seed_list):
    # Calculate the next power of two greater than or equal to the list length
    target_size = next_power_of_two(len(initial_seed_list))

    # Extend the list by adding "bye" to fill up to the target size
    extended_list = initial_seed_list + ["bye"] * (target_size - len(initial_seed_list))

    return extended_list


if __name__ == "__main__":
    # Number of simulations
    num_simulations = 1000000

    # Read match data and set up Elo calculations
    # matches = reader.read_matches_obj("nwsl_matches.txt")
    # # matches = [match for match in matches if match.date <= datetime(2024, 11, 7)]
    # hfa = 45
    # k = 30
    # sr = 0.5511
    # elo_ratings, _, _, _, _ = elo.calculate_elo_ratings(
    #     matches,
    #     print_error=False,
    #     home_field_advantage=hfa,
    #     k=k,
    #     season_reset=sr,
    #     end_date=datetime(2028, 10, 22),
    #     reset_date=datetime(1, 1, 1)
    # )

    matches = reader.read_matches_obj("ncaaf_matches.txt")
    hfa = 60
    k = 77
    sr = 0.0126
    elo_ratings, arr, dates, total_results, dif \
        = elo.calculate_elo_ratings(matches, initial_elo=1000, home_field_advantage=hfa, k=k, season_reset=sr,
                                    end_date=datetime(2029, 3, 1), print_error=False,
                                    reset_date=datetime(1, 3, 1))

    # print(elo_ratings)

    # Seed list for the tournament
    # initial_seed_list = ["Pride", "Spirit", "Gotham", "Current", "Courage", "Thorns", "Bay FC", "Red Stars"]
    # initial_seed_list = ["Oregon", "Georgia", "Boise State", "Arizona State",
    #                      "Texas", "Penn State", "Notre Dame", "Ohio State",
    #                      "Tennessee", "Indiana", "Southern Methodist", "Clemson"]
    initial_seed_list = ["Oregon", "Georgia", "Texas", "Penn State",
                         "Notre Dame", "Ohio State", "Tennessee", "Indiana",
                         "Boise State", "Southern Methodist", "Arizona State", "Clemson"]
    for seed in initial_seed_list:
        print(elo_ratings[seed])
    FINAL_HOST = "Banana"
    # initial_seed_list = ["Wave", "Thorns", "Courage", "Reign", "Angel City", "Gotham"]
    # initial_seed_list = ["Reign", "Thorns", "Wave", "Dash", "Current", "Red Stars"]

    initial_seed_list = extend_to_next_power_of_two(initial_seed_list)
    print(initial_seed_list)

    # Initialize data storage for stats
    round_ct = math.ceil(math.log2(len(initial_seed_list)))
    round_stats = {club: [0] * (round_ct+1) for club in initial_seed_list}  # Each club has a list for each round

    # Simulation loop
    for _ in range(num_simulations):
        # print("START")
        elo_ratings_c = elo_ratings.copy()
        # copy seeds and count them in the opening round
        seed_list = initial_seed_list[:]
        for seed in seed_list:
            # every seed makes round 0
            round_stats[seed][0] += 1

        # tournament loop
        round_number = 0
        while len(seed_list) > 1:
            # if len(seed_list) == 2:
            #     # Check if FINAL_HOST is in the final to give them home-field advantage
            #     if FINAL_HOST in seed_list:
            #         t_hfa = hfa  # Apply home field advantage for FINAL_HOST
            #         # Ensure FINAL_HOST is treated as the home team
            #         if seed_list[0] != FINAL_HOST:
            #             seed_list[0], seed_list[1] = seed_list[1], seed_list[0]
            #     else:
            #         t_hfa = 0  # No home field advantage if FINAL_HOST is not in the final
            # else:
            #     t_hfa = hfa
            if round_number == 0:
                t_hfa = hfa
            else:
                t_hfa = 0

            round_number += 1
            next_round = []

            for i in range(len(seed_list) // 2):
                club1 = seed_list[i]
                club2 = seed_list[-1 - i]

                if len(seed_list) != 2 and club2 != "bye" and initial_seed_list.index(club1) > initial_seed_list.index(club2):
                    club1, club2 = club2, club1
                # if "bye" not in (club1, club2):
                #     print(club1, club2, t_hfa)

                # Calculate win probability for club1
                if club2 == "bye":
                    win_prob = 1
                else:
                    win_prob = elo.expected_result(elo_ratings_c[club1] + t_hfa, elo_ratings_c[club2])
                r = random.random()

                # Determine winner
                if r <= win_prob:
                    winner = club1
                else:
                    winner = club2

                # update elos
                if club1 != "bye":
                    elo_ratings_c[club1] = elo.update_elo(elo_ratings_c[club1], club1 == winner, win_prob, k=k)
                if club2 != "bye":
                    elo_ratings_c[club2] = elo.update_elo(elo_ratings_c[club2], club2 == winner, 1-win_prob, k=k)

                # add the winner to the next round
                next_round.append(winner)
                # and count the winner as being in the next round
                round_stats[winner][round_number] += 1

            seed_list = next_round

    print(f"Tournament Results After {num_simulations:,} Simulations:\n")
    for club, rounds in round_stats.items():
        print(f"{club}:")
        for i, count in enumerate(rounds):
            percentage = (count / num_simulations) * 100
            print(f"  Made it to Round {i + 1}: {percentage:.4f}%")
