from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    findings_csv = ROOT / "results" / "public_repo_findings.csv"
    if not findings_csv.exists():
        print("No public findings available. Run scripts/analyze_public_repositories.py first.")
        raise SystemExit(1)

    rows = []
    with findings_csv.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "repository": row.get("repository", ""),
                "repository_url": row.get("repository_url", ""),
                "path": row.get("path", ""),
                "test_name": row.get("test_name", ""),
                "issue_type": row.get("issue_type", ""),
                "severity": row.get("severity", ""),
                "confidence": row.get("confidence", ""),
                "reviewer_label": "",
                "reviewer_notes": "",
            })

    if not rows:
        print("No findings to review.")
        raise SystemExit(1)

    limit = min(len(rows), 600)
    out = ROOT / "data" / "manual_review_600.csv"
    out.parent.mkdir(exist_ok=True)

    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "repository",
            "repository_url",
            "path",
            "test_name",
            "issue_type",
            "severity",
            "confidence",
            "reviewer_label",
            "reviewer_notes",
        ])
        writer.writeheader()
        writer.writerows(rows[:limit])

    print(f"Saved review-ready dataset: {out} ({len(rows[:limit])} rows)")


if __name__ == "__main__":
    main()
