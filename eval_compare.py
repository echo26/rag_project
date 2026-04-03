"""
Compare RAG vs plain LLM responses for 10 Wikipedia-based questions.
Usage: python eval_compare.py [--api-url http://localhost:8000] [--output results.md]
"""

from __future__ import annotations

import argparse
import asyncio
import time
from dataclasses import dataclass
from datetime import datetime

import httpx

API_URL = "http://localhost:8000"

QUESTIONS = [
    "What is the capital of France and what is it known for?",
    "Who invented the telephone and when was it invented?",
    "What is the largest planet in our solar system and how big is it?",
    "When did World War II end and what were the main causes?",
    "What is the speed of light and why is it important in physics?",
    "Who wrote Romeo and Juliet and during what period did they live?",
    "What is photosynthesis and why is it important for life on Earth?",
    "What is the tallest mountain in the world and how tall is it?",
    "Who was the first person to walk on the moon and when did it happen?",
    "What is DNA and what role does it play in living organisms?",
]


@dataclass
class Result:
    question: str
    no_rag_response: str = ""
    rag_response: str = ""
    no_rag_time: float = 0.0
    rag_time: float = 0.0
    error: str = ""


async def query(client: httpx.AsyncClient, question: str, use_rag: bool) -> tuple[str, float]:
    start = time.monotonic()
    chunks = []
    async with client.stream(
        "POST",
        f"{API_URL}/chat",
        json={"message": question, "use_rag": use_rag},
        timeout=120,
    ) as resp:
        resp.raise_for_status()
        async for chunk in resp.aiter_text():
            chunks.append(chunk)
    elapsed = time.monotonic() - start
    return "".join(chunks).strip(), elapsed


async def evaluate_question(client: httpx.AsyncClient, question: str, idx: int) -> Result:
    result = Result(question=question)
    print(f"\n[{idx}/10] {question}")
    try:
        print("  Running without RAG...", end=" ", flush=True)
        result.no_rag_response, result.no_rag_time = await query(client, question, use_rag=False)
        print(f"done ({result.no_rag_time:.1f}s)")

        print("  Running with RAG...", end=" ", flush=True)
        result.rag_response, result.rag_time = await query(client, question, use_rag=True)
        print(f"done ({result.rag_time:.1f}s)")
    except Exception as e:
        result.error = str(e)
        print(f"ERROR: {e}")
    return result


def render_markdown(results: list[Result]) -> str:
    lines = [
        "# RAG vs Plain LLM Evaluation",
        f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"API: {API_URL}",
        "\n---\n",
    ]
    for i, r in enumerate(results, 1):
        lines.append(f"## Q{i}: {r.question}\n")
        if r.error:
            lines.append(f"**Error:** {r.error}\n")
        else:
            lines.append(f"### Without RAG _(plain LLM, {r.no_rag_time:.1f}s)_\n")
            lines.append(r.no_rag_response)
            lines.append(f"\n\n### With RAG _(vector search + LLM, {r.rag_time:.1f}s)_\n")
            lines.append(r.rag_response)
        lines.append("\n\n---\n")
    return "\n".join(lines)


def render_terminal(results: list[Result]) -> None:
    width = 80
    sep = "=" * width
    for i, r in enumerate(results, 1):
        print(f"\n{sep}")
        print(f"Q{i}: {r.question}")
        print(sep)
        if r.error:
            print(f"ERROR: {r.error}")
            continue
        print(f"\n[WITHOUT RAG - {r.no_rag_time:.1f}s]")
        print(r.no_rag_response)
        print(f"\n[WITH RAG - {r.rag_time:.1f}s]")
        print(r.rag_response)
    print(f"\n{sep}")


async def main(api_url: str, output: str | None) -> None:
    global API_URL
    API_URL = api_url

    print(f"Connecting to {API_URL}...")
    async with httpx.AsyncClient(base_url=api_url) as client:
        # Health check
        try:
            resp = await client.get("/health")
            resp.raise_for_status()
        except Exception as e:
            print(f"API not reachable: {e}")
            return

        results = []
        for i, question in enumerate(QUESTIONS, 1):
            result = await evaluate_question(client, question, i)
            results.append(result)

    render_terminal(results)

    if output:
        md = render_markdown(results)
        with open(output, "w") as f:
            f.write(md)
        print(f"\nResults saved to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare RAG vs plain LLM responses")
    parser.add_argument("--api-url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--output", default="eval_results.md", help="Output markdown file (empty to skip)")
    args = parser.parse_args()

    asyncio.run(main(args.api_url, args.output or None))
