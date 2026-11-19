"""Binary relevance, unique rankings, macro average handled by caller."""
import math

def metrics(ranking, relevant, k=10):
    if k <= 0:
        raise ValueError("k must be positive")
    ranking = list(dict.fromkeys(ranking))[:k]
    relevant = set(relevant)
    if not relevant:
        return None  # Caller must count and report exclusions.
    hits = [int(x in relevant) for x in ranking]
    dcg = sum(v / math.log2(i + 2) for i, v in enumerate(hits))
    idcg = sum(1 / math.log2(i + 2) for i in range(min(k, len(relevant))))
    return {"recall": sum(hits)/len(relevant),
            "hit_rate": float(any(hits)),
            "mrr": next((1/(i+1) for i,v in enumerate(hits) if v), 0.0),
            "ndcg": dcg/idcg}
