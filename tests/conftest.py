import csv
from random import random

import pytest


@pytest.fixture
def csvfile(tmp_path):
    header = ["x", "y", "z"]
    nrows = 10
    filename = tmp_path / "dataset.csv"

    with open(filename, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()

        for _ in range(nrows):
            row = {column: random() for column in header}
            writer.writerow(row)

    return filename
