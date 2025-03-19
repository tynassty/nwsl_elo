import datetime


class Match:
    def __init__(self, date: datetime.datetime, home_club: str, away_club: str, home_score: int = None,
                 away_score: int = None, neutral: bool = False, regular_season: bool = True):
        self.date = date
        self.home_club = home_club
        self.away_club = away_club
        self.home_score = home_score
        self.away_score = away_score
        self.neutral = neutral
        self.regular_season = regular_season

    def is_complete(self):
        return self.home_score is not None and self.away_score is not None

    def winner(self):
        if not self.is_complete():
            return None
        elif self.home_score > self.away_score:
            return self.home_club
        elif self.away_score > self.home_score:
            return self.away_club
        else:
            return "Draw"

    def update_score(self, home_score: int, away_score: int):
        self.home_score = home_score
        self.away_score = away_score

    def is_neutral_site(self):
        return self.neutral

    def __str__(self):
        date_str = self.date.strftime("%Y-%m-%d")
        location = "Neutral Site" if self.neutral else "Home"
        season_type = "Regular Season" if self.regular_season else "Playoffs"

        # Score display: if scores are None, show "TBD"
        if self.home_score is not None and self.away_score is not None:
            score = f"{self.home_score} - {self.away_score}"
        else:
            score = "TBD"

        return (f"{date_str} | {self.home_club:^15} vs {self.away_club:^15} | "
                f"Score: {score} | Location: {location} | {season_type}")

    def __lt__(self, other):
        return self.date < other.date

    def __le__(self, other):
        return self.date <= other.date

    def __eq__(self, other):
        return self.date == other.date

    def __ne__(self, other):
        return self.date != other.date

    def __gt__(self, other):
        return self.date > other.date

    def __ge__(self, other):
        return self.date >= other.date

