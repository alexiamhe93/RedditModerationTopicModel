"""Replicate Analysis 2 inter-rater reliability statistics.

Input:
    SupplementaryMaterials_A_IRR_Analysis2_long.csv

The CSV contains one row per topic x deliberative norm cell, with binary coder
ratings for AG, HB, and MH. Values are 1 = Relevant and 0 = Irrelevant.

Requires:
    pip install krippendorff
"""

from pathlib import Path
import csv

import krippendorff


HERE = Path(__file__).parent
CSV_PATH = HERE / "SupplementaryMaterials_A_IRR_Analysis2_long.csv"
CODERS = ["AG", "HB", "MH"]
NORMS = [
    "Rationality",
    "Interactivity",
    "Equality",
    "Civility",
    "Common good reference",
    "Constructiveness",
]


def load_rows(path):
    rows = []
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            rows.append({
                "TopicID": int(row["TopicID"]),
                "TopicName": row["TopicName"],
                "Norm": row["Norm"],
                "AG": int(row["AG"]),
                "HB": int(row["HB"]),
                "MH": int(row["MH"]),
                "Excluded": row["Excluded"].lower() == "true",
            })
    return rows


def alpha_and_agreement(rows):
    reliability = [[row[coder] for row in rows] for coder in CODERS]
    alpha = krippendorff.alpha(
        reliability_data=reliability,
        level_of_measurement="nominal",
    )
    unanimous = sum(
        1 for row in rows
        if row["AG"] == row["HB"] == row["MH"]
    ) / len(rows)
    pairwise = []
    for row in rows:
        votes = [row[coder] for coder in CODERS]
        matching_pairs = sum(
            1
            for i in range(len(votes))
            for j in range(i + 1, len(votes))
            if votes[i] == votes[j]
        )
        pairwise.append(matching_pairs / 3)
    return alpha, unanimous, sum(pairwise) / len(pairwise)


def relevant_rate(rows):
    votes = [row[coder] for row in rows for coder in CODERS]
    return sum(votes) / len(votes)


def main():
    rows = load_rows(CSV_PATH)
    kept = [row for row in rows if not row["Excluded"]]

    full_alpha, full_unanimous, full_pairwise = alpha_and_agreement(rows)
    kept_alpha, kept_unanimous, kept_pairwise = alpha_and_agreement(kept)

    print("Analysis 2 inter-rater reliability")
    print()
    print(
        "Full set: "
        f"alpha={full_alpha:.3f}; "
        f"unanimous={full_unanimous:.1%}; "
        f"pairwise={full_pairwise:.1%}"
    )
    print(
        "Excluded topics dropped: "
        f"alpha={kept_alpha:.3f}; "
        f"unanimous={kept_unanimous:.1%}; "
        f"pairwise={kept_pairwise:.1%}"
    )
    print()
    print("Per norm, excluded topics dropped:")
    print("Norm,alpha,unanimous,pairwise,pct_relevant")
    for norm in NORMS:
        subset = [row for row in kept if row["Norm"] == norm]
        alpha, unanimous, pairwise = alpha_and_agreement(subset)
        print(
            f"{norm},{alpha:.3f},{unanimous:.1%},"
            f"{pairwise:.1%},{relevant_rate(subset):.0%}"
        )


if __name__ == "__main__":
    main()
