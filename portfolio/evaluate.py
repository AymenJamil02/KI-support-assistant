"""Reproducible baseline evaluation. No paid calls or LLM-quality claims."""
import json
from pathlib import Path
import statistics

from portfolio.assistant import KnowledgeAssistant

ROOT = Path(__file__).resolve().parent.parent


def evaluate() -> dict:
    assistant = KnowledgeAssistant()
    questions = json.loads((ROOT / "data/questions.json").read_text(encoding="utf-8"))
    results = []
    for item in questions:
        result = assistant.answer(item["question"])
        source_ids = [s["id"] for s in result["sources"]]
        expected = item["source"]
        passed = result["abstained"] if expected is None else (not result["abstained"] and expected in source_ids)
        results.append({**item, "returned_sources": source_ids, "abstained": result["abstained"], "passed": passed, "elapsed_ms": result["elapsed_ms"]})
    known = [r for r in results if r["source"] is not None]
    unknown = [r for r in results if r["source"] is None]
    return {"mode": "extractive", "total": len(results), "passed": sum(r["passed"] for r in results), "source_recall": sum(r["passed"] for r in known) / len(known), "unknown_abstention_rate": sum(r["passed"] for r in unknown) / len(unknown), "median_ms": round(statistics.median(r["elapsed_ms"] for r in results), 2), "limitations": "Kleine handgeschriebene Entwicklungs-Testmenge. Keine unabhängige Validierung; kein Nachweis für LLM-Antwortqualität oder Produktionsreife. Quellen-Recall prüft enthaltene erwartete Quelle, nicht jede Aussage.", "results": results}


def main() -> None:
    result = evaluate()
    target = ROOT / "reports"
    target.mkdir(exist_ok=True)
    (target / "evaluation.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "results"}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
