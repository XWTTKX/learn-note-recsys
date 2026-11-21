"""Audit achievable recall and ItemCF history coverage on a chronological split."""
import argparse
import json
from pathlib import Path

from recommender import Recommender, temporal_split


def audit(test, model, limit):
    counted = total = oov = recoverable = history_covered = 0
    ceilings = []
    for request in test:
        seen = set(request["history"])
        relevant = {x["id"] for x in request["candidates"] if x["click"] == 1} - seen
        if not relevant:
            continue
        counted += 1
        available = len(relevant & model.catalog)
        total += len(relevant)
        oov += len(relevant) - available
        recoverable += min(limit, available)
        ceilings.append(min(limit, available) / len(relevant))
        history_covered += any(item in model.sim for item in seen)
    return {
        "test_requests": len(test),
        "excluded_no_positive": len(test) - counted,
        "k": limit,
        "positive_oov_rate": oov / total if total else None,
        "macro_recall_upper_bound": sum(ceilings) / counted if counted else None,
        "micro_recall_upper_bound": recoverable / total if total else None,
        "valid_requests_with_itemcf_seed": history_covered / counted if counted else None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--data", type=Path, default=root / "data/sample/requests.jsonl")
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()
    if args.k <= 0:
        parser.error("--k must be positive")
    with args.data.open(encoding="utf-8") as stream:
        rows = [json.loads(line) for line in stream if line.strip()]
    train, test = temporal_split(rows)
    print(json.dumps(audit(test, Recommender(train), args.k), ensure_ascii=False))


if __name__ == "__main__":
    main()
