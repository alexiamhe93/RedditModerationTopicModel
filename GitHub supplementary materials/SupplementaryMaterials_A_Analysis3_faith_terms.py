"""
Supplementary Materials A -- Analysis 3 (good/bad faith term prevalence).

Reproduces the prevalence figures reported in Results 4.3 of the manuscript.

The raw interview corpus is NOT distributed (it contains identifiable participant
speech). This script reads a private corpus file with one row per interview turn
and the columns: Speaker, Text, Topic. It writes only DERIVED outputs that contain
no raw text:

  - SupplementaryMaterials_A_Analysis3_speaker_flags.csv : per-speaker booleans
  - SupplementaryMaterials_A_Analysis3_term_counts.csv   : per-term turn counts

Run: python3 SupplementaryMaterials_A_Analysis3_faith_terms.py <corpus.csv>
"""
import sys
import re
import pandas as pd

N_MODERATORS = 32  # denominator for prevalence percentages

# Term dictionary used to flag discussion of user intentions (good/bad faith).
EXPLICIT = ["good faith", "bad faith"]
SYNONYMS = [
    "bad people", "bad actor", "bad person", "ill intentions", "mean people",
    "purposefully misunderstands", "ulterior motive", "intentionally harmful",
    "hateful people", "disingenuous", "specific agenda", "troll",
    "good people", "wellmeaning", "wellintended", "being genuine",
]
ALL_TERMS = EXPLICIT + SYNONYMS


def _matches(terms, text):
    pattern = "|".join(re.escape(t) for t in terms)
    return bool(re.search(pattern, str(text), flags=re.IGNORECASE))


def main(corpus_path):
    df = pd.read_csv(corpus_path).dropna(subset=["Text"])

    # Per-speaker flags (verifies the moderator-level prevalence counts).
    by_speaker = df.groupby("Speaker")["Text"].apply(" ".join)
    flags = pd.DataFrame({
        "Speaker": by_speaker.index,
        "mentions_explicit": [_matches(EXPLICIT, t) for t in by_speaker],
        "mentions_synonym": [_matches(ALL_TERMS, t) for t in by_speaker],
    })
    flags.to_csv("SupplementaryMaterials_A_Analysis3_speaker_flags.csv", index=False)

    # Per-term turn counts (frequency of each dictionary term across turns).
    term_counts = pd.DataFrame({
        "term": ALL_TERMS,
        "class": ["explicit"] * len(EXPLICIT) + ["synonym"] * len(SYNONYMS),
        "n_turns": [int(df["Text"].str.contains(re.escape(t), case=False, na=False).sum())
                    for t in ALL_TERMS],
    })
    term_counts.to_csv("SupplementaryMaterials_A_Analysis3_term_counts.csv", index=False)

    n_explicit = int(flags["mentions_explicit"].sum())
    n_synonym = int(flags["mentions_synonym"].sum())
    faith_turns = df[df["Text"].str.contains("|".join(re.escape(t) for t in ALL_TERMS),
                                             case=False, na=False)]
    n_topics = faith_turns["Topic"].nunique()

    print(f"Explicit good/bad faith: {n_explicit} moderators "
          f"({n_explicit / N_MODERATORS * 100:.1f}%)")
    print(f"Including synonyms:      {n_synonym} moderators "
          f"({n_synonym / N_MODERATORS * 100:.1f}%)")
    print(f"Topics with faith discussion: {n_topics}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "DocumentsWithTopics.csv")
