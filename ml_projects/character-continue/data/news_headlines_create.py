import csv
import json
import unicodedata
import pathlib

directory = pathlib.Path(__file__).parent.absolute()

def normalize(message: str) -> str:
    nfkd_form = unicodedata.normalize('NFKD', message)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

# {"link": "https://www.huffpost.com/entry/covid-boosters-uptake-us_n_632d719ee4b087fae6feaac9", "headline": "Over 4 Million Americans Roll Up Sleeves For Omicron-Targeted COVID Boosters", "category": "U.S. NEWS", "short_description": "Health experts said it is too early to predict whether demand would match up with the 171 million doses of the new boosters the U.S. ordered for the fall.", "authors": "Carla K. Johnson, AP", "date": "2022-09-23"}

total = 0

with open(directory / "archive" / "News_Category_Dataset_v3.json", "r", encoding="utf-8") as in_file:
    with open(directory / "news_headlines.txt", "w", encoding="utf-8", newline='') as out_file:
        for line in in_file:
            data = json.loads(line)
            if "headline" not in data or "category" not in data or "authors" not in data or "date" not in data:
                continue
            out_file.write(data["category"] + ": " + data["headline"] + ", " + data["authors"] + ", " + data["date"] + "\n")
            total += 1


print(f"Total headlines processed: {total}")
print(f"Output written to: {directory / 'news_headlines.txt'}")
            