import csv
import unicodedata

def normalize(message: str) -> str:
    nfkd_form = unicodedata.normalize('NFKD', message)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


# --- Read Write ---

# with open(input_filename, 'r', encoding="utf-8") as file:
#     content = file.read()

# modified_content = content.replace('. ', '.\n')

# with open(output_filename, 'w', encoding="utf-8") as file:
#     file.write(modified_content)

# print(f"Newlines inserted after periods and saved to {output_filename}")

# --- Read Write ---

# with open("test.csv", "r", encoding="utf-8") as file:
#     data = csv.reader(file.readlines())
#     messages = [normalize(line[3]) for line in data if len(line) > 3]

# with open("test.txt", "w", encoding="utf-8") as file:
#     file.writelines(messages)
    
# --- Read Write ---
    
# with open("starwars.csv", "r", encoding="utf-8") as file:
#     data = [line.split('" "')[-1][:-2] + "\n" for line in file.readlines()]

# with open("starwars.txt", "w", encoding="utf-8") as file:
#     file.writelines(data)

# --- Read Write ---

