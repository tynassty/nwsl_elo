import re
from unidecode import unidecode
from datetime import datetime
import csv

from Match import Match

clubs_to_replace = ["Sky Blue", "Flash"]
replacement_clubs = ["Gotham", "Courage"]

club_replacements = {
    "Sky Blue": "Gotham",
    "Flash": "Courage",
    "San Antonio Stars": "Las Vegas Aces",
    "San Antonio Silver Stars": "Las Vegas Aces",
    "Utah Starzz": "Las Vegas Aces",
    "Tulsa Shock": "Dallas Wings",
    "Detroit Shock": "Dallas Wings",
    "Orlando Miracle": "Connecticut Sun"
}


def replace_club(club_name):
    # Replace club name if it's in the dictionary, otherwise return the original name
    return club_replacements.get(club_name, club_name)


def read_matches_obj(match_file):
    matches = []
    f = open(match_file, encoding="utf8")

    for line in f:
        line = line.split(", ")
        line[-1] = line[-1][:-1]
        date = datetime.strptime(line[0], "%Y-%m-%d")
        home_club = clean_name(line[1])
        away_club = clean_name(line[2])
        home_score = line[3]
        away_score = line[4]
        if line[5] == "@":
            temp = home_club
            home_club = away_club
            away_club = temp
            temp = home_score
            home_score = away_score
            away_score = temp
        if line[5] == "N":
            neutral = True
        else:
            neutral = False

        if len(line) > 6 and line[6] == "TRUE":
            regular_season = True
        else:
            regular_season = False

        if home_club in club_replacements:
            home_club = replace_club(home_club)

        if away_club in club_replacements:
            away_club = replace_club(away_club)

        if home_club == "Royals" and date.year <= 2023:
            home_club = "Royals (2018)"

        if away_club == "Royals" and date.year <= 2023:
            away_club = "Royals (2018)"


        home_score = int(home_score)
        away_score = int(away_score)

        m = Match(date, home_club, away_club, home_score=home_score, away_score=away_score,
                  neutral=neutral, regular_season=regular_season)

        matches.append(m)

    return matches


def read_matches(match_file):
    matches = []
    f = open(match_file, encoding="utf8")

    for line in f:
        line = line.split(", ")
        line[-1] = line[-1][:-1]
        date = datetime.strptime(line[0], "%Y-%m-%d")
        home_club = clean_name(line[1])
        away_club = clean_name(line[2])
        home_score = line[3]
        away_score = line[4]
        if line[5] == "@":
            temp = home_club
            home_club = away_club
            away_club = temp
            temp = home_score
            home_score = away_score
            away_score = temp
        if line[5] == "N":
            neutral = True
        else:
            neutral = False

        if home_club in club_replacements:
            home_club = replace_club(home_club)

        if away_club in club_replacements:
            away_club = replace_club(away_club)

        matches.append((date, home_club, away_club, home_score, away_score, neutral))

    return matches


def read_matches_2(match_file):
    matches = []

    with open(match_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL)

        for row in reader:
            if row[6] == "true":
                date = datetime.strptime(row[4], "%Y-%m-%dT%H:%M:%S.%fZ")
                date = datetime(date.year, date.month, date.day)
                home_club = row[13]
                home_score = int(row[16])
                away_club = row[25]
                away_score = int(row[28])
                if row[7] == "true":
                    neutral = True
                else:
                    neutral = False

            matches.append((date, home_club, away_club, home_score, away_score, neutral))
    # for match in matches:
    #     print(match[0])
    return matches


def clean_name(state_name):
    # Use regex to remove any numbers, parentheses, and leading/trailing spaces
    cleaned_name = re.sub(r'\(\d+\)', '', state_name).strip()
    return cleaned_name


if __name__ == '__main__':
    # matches = read_matches("nwsl_matches.txt")
    # for match in matches:
    #     print(match)

    matches = read_matches_obj("nwsl_matches.txt")
    for match in matches:
        print(match)

