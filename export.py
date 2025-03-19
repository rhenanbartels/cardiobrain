import csv


def export_as_csv(file_path, results, columns):
    with open(file_path, "w") as fobj:
        w = csv.DictWriter(fobj, columns)
        w.writeheader()
        w.writerow({c: results[c] for c in columns})

