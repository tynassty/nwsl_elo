import reader


class Club:
    def __init__(self, name):
        self.name = name
        self.games_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_scored = 0
        self.goals_conceded = 0
        self.points = 0

    def update_stats(self, goals_for, goals_against):
        self.games_played += 1
        self.goals_scored += goals_for
        self.goals_conceded += goals_against
        if goals_for > goals_against:
            self.wins += 1
            self.points += 3
        elif goals_for == goals_against:
            self.draws += 1
            self.points += 1
        else:
            self.losses += 1

    def goal_difference(self):
        return self.goals_scored - self.goals_conceded

    def deduct_points(self, points):
        self.points -= points

    def __str__(self):
        return (f"{self.name:<12} {self.points:>3} pts, {self.games_played:>2} GP, "
                f"{self.wins:>2} W, {self.draws:>2} D, {self.losses:>2} L, "
                f"{self.goals_scored:>2} GF, {self.goals_conceded:>2} GA, GD {self.goal_difference():>3}")


class LeagueTable:
    def __init__(self):
        self.clubs = {}

    def add_club(self, name):
        if name not in self.clubs:
            self.clubs[name] = Club(name)

    def record_match(self, club1, club2, goals1, goals2):
        self.add_club(club1)
        self.add_club(club2)
        self.clubs[club1].update_stats(goals1, goals2)
        self.clubs[club2].update_stats(goals2, goals1)

    def standings(self):
        sorted_clubs = sorted(self.clubs.values(), key=lambda x: (x.points, x.goal_difference(), x.goals_scored),
                              reverse=True)
        for idx, club in enumerate(sorted_clubs, 1):
            print(f"{idx:>2}. {club}")

    def deduct_points(self, club_name, points):
        if club_name in self.clubs:
            self.clubs[club_name].deduct_points(points)

    def __str__(self):
        to_return = ""
        sorted_clubs = sorted(self.clubs.values(), key=lambda x: (x.points, x.goal_difference(), x.goals_scored),
                              reverse=True)
        for idx, club in enumerate(sorted_clubs, 1):
            to_return += f"{idx:>2}. {club}\n"
        return to_return


if __name__ == "__main__":
    # Example usage
    league = LeagueTable()

    matches = reader.read_matches_obj("nwsl_matches.txt")
    matches = [match for match in matches if match.date.year == 2024]
    big_boys = ("Pride", "Current", "Spirit")
    matches = [match for match in matches if any(item in big_boys for item in (match.home_club, match.away_club))]
    for match in matches:
        league.record_match(match.home_club, match.away_club, match.home_score, match.away_score)

    league.standings()
