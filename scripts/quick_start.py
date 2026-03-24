#!/usr/bin/env python3
# flake8: noqa: E402
"""Quick Start Script for Speech Front-end Daily"""

import os
import sys
from datetime import date, datetime

# Make sure src is on the import path
ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

from src.arxiv_fetcher import fetch_arxiv_papers
from src.filter import filter_papers
from src.paper_detail import fetch_paper_details
from src.html_generator import generate_html
from src.evaluator import evaluate_paper


def main():
    api_key = os.environ.get("OPENAI_API_KEY", None)
    max_papers = 8

    papers = fetch_arxiv_papers(max_papers=max_papers)
    papers = filter_papers(papers)

    target_papers = papers[:max_papers]
    for p in target_papers:
        p.update(fetch_paper_details(p["arxiv_id"]))
        if not p.get("category"):
            try:
                from src.filter import assign_category

                p["category"] = assign_category(p)
            except Exception:
                p["category"] = "Other"

    if api_key:
        for i, p in enumerate(target_papers[:3], 1):
            print(f"Evaluating {p.get('arxiv_id')} ({i}/{len(target_papers)}) ...")
            res = evaluate_paper(p, api_key)
            p.update(res)
    else:
        print("OPENAI_API_KEY not found; skipping LLM evaluation in quick_start.")

    date_str = date.today().strftime("%Y%m%d")
    output_path = os.path.join(ROOT, "src", "tmp", f"speech_daily_{date_str}.html")
    html = generate_html(target_papers, datetime.now())
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
