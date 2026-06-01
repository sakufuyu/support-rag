import json
import time
import requests

API_URL = "http://localhost:8000/query"
ACCESS_CODE = "demo-access-code"


def keyword_coverage(answer: str, expected_keywords: list[str]) -> float:
    answer_lower = answer.lower()
    hits = 0

    if not expected_keywords:
        return 0.0

    for keyword in expected_keywords:
        if keyword.lower() in answer_lower:
            hits += 1

    return hits / len(expected_keywords)


def main():
    with open("evals/support_qa.json", "r") as f:
        cases = json.load(f)

    results = []
    for case in cases:
        start = time.time()

        response = requests.post(
            API_URL,
            json={
                "question": case["question"],
                "access_code": ACCESS_CODE,
            },
            timeout=60,
        )

        elapsed = time.time() - start
        response.raise_for_status()

        data = response.json()
        answer = data["answer"]
        sources = data["sources"]

        source_hit = any(
            source["filename"] == case["expected_source"] for source in sources
        )

        coverage = keyword_coverage(answer, case["expected_keywords"])

        results.append(
            {
                "question": case["question"],
                "source_hit": source_hit,
                "keyword_coverage": coverage,
                "latency_seconds": round(elapsed, 2),
                "answer": answer,
            }
        )
    
    total = len(results)
    retrieval_hit_rate = sum(1 for r in results if r["source_hit"]) / total
    avg_keyword_coverage = sum(r["keyword_coverage"] for r in results) / total
    avg_latency = sum(r["latency_seconds"] for r in results) / total

    report = {
        "retrieval_hit_rate": retrieval_hit_rate,
        "avg_keyword_coverage": avg_keyword_coverage,
        "avg_latency_seconds": avg_latency,
        "results": results,
    }
    print(json.dumps(report, indent=2))

    with open("evals/docs/eval-report.md", "w") as f:
        f.write("# Eval Report\n\n")
        f.write(f"- Retrieval hit rate: {retrieval_hit_rate:.2%}\n")
        f.write(f"- Average keyword coverage: {avg_keyword_coverage:.2%}\n")
        f.write(f"- Average latency: {avg_latency:.2f}s\n\n")

        for result in results:
            f.write(f"## {result['question']}\n\n")
            f.write(f"- Source hit: {result['source_hit']}\n")
            f.write(f"- Keyword coverage: {result['keyword_coverage']:.2%}\n")
            f.write(f"- Latency: {result['latency_seconds']}s\n\n")
            f.write("### Answer\n\n")
            f.write(result["answer"])
            f.write("\n\n")


if __name__ == "__main__":
    main()
