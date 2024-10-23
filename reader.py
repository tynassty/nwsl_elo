import re
from unidecode import unidecode
from datetime import datetime
import csv

clubs_to_replace = ["Sky Blue", "Flash"]
replacement_clubs = ["Gotham", "Courage"]


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
        if home_club in clubs_to_replace:
            home_club = replacement_clubs[clubs_to_replace.index(home_club)]
        if away_club in clubs_to_replace:
            away_club = replacement_clubs[clubs_to_replace.index(away_club)]
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


    # matches = []
    # f = open(match_file, encoding="utf8")
    #
    # for line in f:
    #     line = line.split(",")
    #     cleaned_line = [cell.strip('"') for cell in line]
    #     date = datetime.strptime(cleaned_line[4].strip('"'), "%Y-%m-%dT%H:%M:%S.%fZ")
    #     home_club = cleaned_line[13]
    #     home_score = int(cleaned_line[16])
    #     away_club = cleaned_line[25]
    #     away_score = int(cleaned_line[28])
    #     print(home_club + " " + str(home_score) + "-" + str(away_score) + " " + away_club)
    #
    # return matches


def clean_name(state_name):
    # Use regex to remove any numbers, parentheses, and leading/trailing spaces
    cleaned_name = re.sub(r'\(\d+\)', '', state_name).strip()
    return cleaned_name


if __name__ == '__main__':
    # matches = read_matches("nwsl_matches.txt")
    # for match in matches:
    #     print(match)

    matches = read_matches_2("ncaaf2.txt")
    for match in matches:
        print(match)

