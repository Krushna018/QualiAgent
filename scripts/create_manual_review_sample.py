
from pathlib import Path
import json, random, csv

ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest = json.loads((ROOT/"data"/"benchmark_manifest.json").read_text())
    random.seed(7)

    # Stratified 600-item review sample: 100 examples from each of 6 issue classes.
    by_label = {}
    for x in manifest:
        by_label.setdefault(x["label"], []).append(x)

    sample = []
    for label, rows in sorted(by_label.items()):
        random.shuffle(rows)
        sample.extend(rows[:100])

    random.shuffle(sample)
    out = ROOT/"data"/"manual_review_600.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "repository","path","test_name","label",
            "reviewer_label","reviewer_notes"
        ])
        w.writeheader()
        for x in sample:
            w.writerow({**x, "reviewer_label":"", "reviewer_notes":""})

    print("Manual-review sample:", len(sample))
    print("Saved:", out)

if __name__ == "__main__":
    main()
