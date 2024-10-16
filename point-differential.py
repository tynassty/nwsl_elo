import reader

matches = reader.read_matches("ncaaf.txt")
for match in matches:
    print(match[0])
print(len(matches))
