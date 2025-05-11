import csv
from pathlib import Path


def export_as_csv(file_path, results, columns):
    file_path = Path(file_path)
    file_exists = file_path.exists()
    with open(file_path, "a") as fobj:
        w = csv.DictWriter(fobj, columns)
        if not file_exists:
            w.writeheader()
        w.writerow({c: results[c] for c in columns})

