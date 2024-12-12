from datetime import datetime

FIRST_DATE = datetime(1953, 3, 1)
FINAL_DATE = datetime.today()

ACC = ["Florida State", "Louisville", "North Carolina State", "Georgia Tech", "Virginia Tech", "North Carolina",
       "Clemson", "Duke", "Miami (FL)", "Boston College", "Syracuse", "Virginia", "Pittsburgh", "Wake Forest",
       "Southern Methodist", "California", "Stanford", "South Carolina", "Maryland", "Notre Dame"]
ACC_CURRENT = ["Florida State", "Louisville", "North Carolina State", "Georgia Tech", "Virginia Tech", "North Carolina",
               "Clemson", "Duke", "Miami (FL)", "Boston College", "Syracuse", "Virginia", "Pittsburgh", "Wake Forest",
               "Southern Methodist", "California", "Stanford"]
OLD_ACC = ["Florida State", "Louisville", "North Carolina State", "Georgia Tech", "Virginia Tech", "North Carolina",
           "Clemson", "Duke", "Miami (FL)", "Boston College", "Syracuse", "Virginia", "Pittsburgh", "Wake Forest"]
CLASSIC_ACC = ["Clemson", "Duke", "Maryland", "North Carolina", "North Carolina State", "Wake Forest", "Virginia",
               "Georgia Tech", "Florida State"]
ACC_A = ["Boston College", "Clemson", "Florida State", "Louisville", "North Carolina State", "Syracuse", "Wake Forest"]
ACC_C = ["Virginia Tech", "Georgia Tech", "Miami (FL)", "Virginia", "North Carolina", "Pittsburgh", "Duke"]
SEC = ["Texas", "Oklahoma", "Florida", "Georgia", "Vanderbilt", "Kentucky", "Missouri", "Texas A&M", "Arkansas",
       "Louisiana State", "Tennessee", "Mississippi", "Mississippi State", "Auburn", "Alabama", "South Carolina",
       "Georgia Tech", "Tulane"]
SEC_CURRENT = ["Texas", "Oklahoma", "Florida", "Georgia", "Vanderbilt", "Kentucky", "Missouri", "Texas A&M", "Arkansas",
               "Louisiana State", "Tennessee", "Mississippi", "Mississippi State", "Auburn", "Alabama",
               "South Carolina"]
SEC_E = ["Kentucky", "Tennessee", "Florida", "Georgia", "Missouri", "Vanderbilt", "South Carolina"]
SEC_W = ["Alabama", "Louisiana State", "Mississippi", "Texas A&M", "Auburn", "Arkansas", "Mississippi State"]
MAC = ["Buffalo", "Eastern Michigan", "Central Michigan", "Ohio", "Toledo", "Bowling Green", "Miami (OH)",
       "Western Michigan", "Northern Illinois", "Ball State", "Akron", "Kent State"]
CLASSIC_BIGEAST = ["Miami (FL)", "West Virginia", "Pittsburgh", "Virginia Tech", "Boston College", "Temple",
                   "Syracuse", "Rutgers"]
B10_CURRENT = ["UCLA", "Illinois", "Indiana", "Iowa", "Maryland", "Michigan", "Michigan State", "Minnesota", "Nebraska",
               "Northwestern", "Ohio State", "Oregon", "Penn State", "Purdue", "Rutgers", "Southern California",
               "Washington", "Wisconsin"]
XII_CURRENT = ["Arizona", "Arizona State", "Baylor", "Brigham Young", "Central Florida", "Cincinnati", "Colorado",
               "Houston", "Iowa State", "Kansas", "Kansas State", "Oklahoma State", "Texas Christian", "Texas Tech",
               "Utah", "West Virginia"]
OLD_PAC_NORTH = ["Washington", "Oregon State", "Oregon", "Washington State", "California", "Stanford"]
OLD_PAC_SOUTH = ["Southern California", "UCLA", "Utah", "Arizona", "Arizona State", "Colorado"]
OLD_PAC = OLD_PAC_NORTH + OLD_PAC_SOUTH
IVY = ["Harvard", "Yale", "Brown", "Pennsylvania", "Dartmouth", "Cornell", "Columbia", "Princeton"]
sec_metadata = {
    "Georgia Tech":      (FIRST_DATE, datetime(1964, 3, 1), "#B3A369"),
    "Tulane":            (FIRST_DATE, datetime(1966, 3, 1), "#006747"),
    "Alabama":           (FIRST_DATE, FINAL_DATE, "#9e1b32", "#828a8f"),
    "Auburn":            (FIRST_DATE, FINAL_DATE, "#0C2340", "#E87722"),
    "Florida":           (FIRST_DATE, FINAL_DATE, "#FA4616", "#0021A5"),
    "Georgia":           (FIRST_DATE, FINAL_DATE, "#BA0C2F"),
    "Kentucky":          (FIRST_DATE, FINAL_DATE, "#0033a0"),
    "Louisiana State":   (FIRST_DATE, FINAL_DATE, "#461D7C", "#FDD023"),
    "Mississippi":       (FIRST_DATE, FINAL_DATE, "#CE1126", "#14213D"),
    "Mississippi State": (FIRST_DATE, FINAL_DATE, "#660000"),
    "Tennessee":         (FIRST_DATE, FINAL_DATE, "#FF8200"),
    "Vanderbilt":        (FIRST_DATE, FINAL_DATE, "#866d4b"),
    "Arkansas":          (datetime(1992, 3, 1), FINAL_DATE, "#9D2235"),
    "South Carolina":    (datetime(1992, 3, 1), FINAL_DATE, "#73000A"),
    "Texas A&M":         (datetime(2012, 3, 1), FINAL_DATE, "#500000", "#FFFFFF"),
    "Missouri":          (datetime(2012, 3, 1), FINAL_DATE, "#F1B82D", "#000000"),
    "Oklahoma":          (datetime(2024, 3, 1), FINAL_DATE, "#841617", "#FDF9D8"),
    "Texas":             (datetime(2024, 3, 1), FINAL_DATE, "#bf5700"),
}
acc_metadata = {
    "Boston College": (datetime(2005, 3, 1), FINAL_DATE, "#98002E", "#BC9B6A"),
    "Clemson": (FIRST_DATE, FINAL_DATE, "#F56600"),
    "Florida State": (datetime(1992, 3, 1), FINAL_DATE, "#782F40", "#CEB888"),
    "Louisville": (datetime(2014, 3, 1), FINAL_DATE, "#000000", "#AD0000"),
    "North Carolina State": (FIRST_DATE, FINAL_DATE, "#CC0000", "#000000"),
    "Syracuse": (datetime(2013, 3, 1), FINAL_DATE, "#F76900", "#000E54"),
    "Wake Forest": (FIRST_DATE, FINAL_DATE, "#9E7E38", "#000000"),
    "Virginia Tech": (datetime(2004, 3, 1), FINAL_DATE, "#630031", "#cf4420"),
    "Georgia Tech": (datetime(1983, 3, 1), FINAL_DATE, "#B3A369"),
    "Miami (FL)": (datetime(2004, 3, 1), FINAL_DATE, "#005030"),
    "Virginia": (datetime(1954, 3, 1), FINAL_DATE, "#232D4B", "#F84C1E"),
    "North Carolina": (FIRST_DATE, FINAL_DATE, "#7BAFD4"),
    "Pittsburgh": (datetime(2013, 3, 1), FINAL_DATE, "#FFB81C"),
    "Duke": (FIRST_DATE, FINAL_DATE, "#003087"),
    "South Carolina": (FIRST_DATE, datetime(1971, 3, 1), "#73000A"),
    "Maryland": (FIRST_DATE, datetime(2014, 3, 1), "#E03a3e", "#ffd520"),
    "Southern Methodist": (datetime(2024, 3, 1), FINAL_DATE, "#C8102E"),
    "California": (datetime(2024, 3, 1), FINAL_DATE, "#FDB515", "#003262"),
    "Stanford": (datetime(2024, 3, 1), FINAL_DATE, "#8C1515"),
    "Notre Dame": (datetime(2020, 3, 1), datetime(2021, 3, 1), "#c99700"),
}
