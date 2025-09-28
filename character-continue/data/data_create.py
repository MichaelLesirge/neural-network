import csv
import unicodedata
import pathlib

directory = pathlib.Path(__file__).parent.absolute() / "dataset"

def normalize(message: str) -> str:
    nfkd_form = unicodedata.normalize('NFKD', message)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


# --- Read Write ---

def sentences_to_lines(input_filename, output_filename):
    with open(input_filename, 'r', encoding="utf-8") as file:
        content = file.read()

    modified_content = content.replace('. ', '.\n')

    with open(output_filename, 'w', encoding="utf-8") as file:
        file.write(modified_content)

def csv_to_txt(input, column_index, ending="\n"):
    with open(directory / input, "r", encoding="utf-8") as file:
        data = csv.reader(file.readlines())
        messages = [normalize(line[column_index])+ending for line in data if len(line) > 3]

    with open(directory / "data.txt", "w", encoding="utf-8") as file:
        file.writelines(messages)
    
def starwars():
    with open("starwars.csv", "r", encoding="utf-8") as file:
        data = [line.split('" "')[-1][:-2] + "\n" for line in file.readlines()]

    with open("starwars.txt", "w", encoding="utf-8") as file:
        file.writelines(data)


def python():
    import os
    def get_python_files(path):
        python_files = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    if ".venv" not in file_path:
                        python_files.append(file_path)
        return python_files

    data = []
    for path in get_python_files(directory.parent.parent):
        print(path)
        with open(path, "r", encoding="utf-8") as file:
            data.extend(file.readlines())

    with open(directory / "data.txt", "w", encoding="utf-8") as file:
        file.writelines([line for line in data if len(line) > 4])

# python()
csv_to_txt("The_Office_lines.csv", 4)