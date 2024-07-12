from unidecode import unidecode
from datetime import datetime

clubs_to_replace = ["Sky Blue", "Flash"]
replacement_clubs = ["Gotham", "Courage"]


def read_matches(match_file):
    matches = []
    f = open(match_file, encoding="utf8")

    for line in f:
        line = line.split(", ")
        line[-1] = line[-1][:-1]
        date = datetime.strptime(line[0], "%Y-%m-%d")
        home_club = line[1]
        away_club = line[2]
        home_score = line[3]
        away_score = line[4]
        if home_club in clubs_to_replace:
            home_club = replacement_clubs[clubs_to_replace.index(home_club)]
        if away_club in clubs_to_replace:
            away_club = replacement_clubs[clubs_to_replace.index(away_club)]
        matches.append((date, home_club, away_club, home_score, away_score))

    return matches


if __name__ == '__main__':
    matches = read_matches("matches.txt")
    for match in matches:
        print(match)
