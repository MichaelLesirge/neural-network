import numpy as np

# https://www.kaggle.com/datasets/rtatman/ubuntu-dialogue-corpus

"""
import tarfile
import csv

def get_csv_from_tar(tar: tarfile.TarFile, member: str):
    with tar.extractfile(member) as file:
        csv_data = csv.reader(line.decode() for line in file.readlines())
    return csv_data

file = "amazon_review_full_csv.tar.gz"

with tarfile.open(file, "r:gz") as tar:
    name = file.split(".")[0]
    train = get_csv_from_tar(tar, name + "/train.csv")
    test = get_csv_from_tar(tar, name + "/test.csv")

all_text_data = np.array([review_body.lower() for (rating, title, review_body) in train] + [review_body.lower() for (rating, title, review_body) in test])
np.save("rating-bodies.npy", all_text_data)
"""
