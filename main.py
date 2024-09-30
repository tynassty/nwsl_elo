import elo
import reader

ACC = ["Florida State", "Louisville", "North Carolina State", "Georgia Tech", "Virginia Tech", "North Carolina",
       "Clemson", "Duke", "Miami (FL)", "Boston College", "Syracuse", "Virginia", "Pittsburgh", "Wake Forest",
       "Southern Methodist", "California", "Stanford"]
SEC = ["Texas", "Oklahoma", "Florida", "Georgia", "Vanderbilt", "Kentucky", "Missouri", "Texas A&M", "Arkansas",
       "Louisiana State", "Tennessee", "Mississippi", "Mississippi State", "Auburn", "Alabama", "South Carolina"]
MAC = ["Buffalo", "Eastern Michigan", "Central Michigan", "Ohio", "Toledo", "Bowling Green", "Miami (OH)",
       "Western Michigan", "Northern Illinois", "Ball State", "Akron", "Kent State"]

matches = reader.read_matches("ncaaf.txt")
elo_ratings, arr, dates, total_results, dif \
    = elo.calculate_elo_ratings(matches, initial_elo=1000, home_field_advantage=72, k=52, season_reset=False)

# for elo_rating in elo_ratings:
#     print(elo_rating, elo_ratings[elo_rating])
sorted_elos = sorted(elo_ratings, key=elo_ratings.get)
for elo_rating in sorted_elos:
    print(elo_rating, elo_ratings[elo_rating])

clubs = ["Georgia", "Alabama", "Michigan", "Ohio State", "Texas", "Oregon", "Clemson", "Notre Dame", "Tennessee",
         "Penn State", "Louisiana State", "Washington"]
elo.plot_elo_ratings_over_time(arr, dates, clubs)
