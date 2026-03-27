"""Full-text extraction utilities for papers"""

import os
import urllib.request
import html
from typing import Optional


def download_pdf(url: str, dest_path: str) -> bool:
    """Download a PDF from url to dest_path. Returns True on success, False on failure."""
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        urllib.request.urlretrieve(url, dest_path)
        return True
    except Exception:
        return False


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file. Returns empty string on failure."""
    try:
        # pdfminer.six is a common choice; fall back gracefully if not installed
        from pdfminer.high_level import extract_text  # type: ignore

        return extract_text(pdf_path)
    except Exception:
        return ""


def parse_full_text(text: str) -> dict:
    """Very lightweight full-text parser to extract core fields.
    Returns a dict with keys: core_innovations, datasets, experimental_parameters, results, limitations, analysis_summary
    This is a heuristic approach intended as a MVP; it can be adjusted for precision.
    """
    if not text:
        return {
            "core_innovations": "",
            "datasets": "",
            "experimental_parameters": "",
            "results": "",
            "limitations": "",
            "analysis_summary": "",
        }

    lines = text.splitlines()
    blocks = {
        "core_innovations": [],
        "datasets": [],
        "experimental_parameters": [],
        "results": [],
        "limitations": [],
    }

    # simple heading-based parser
    current: Optional[str] = None
    synonyms = {
        "core_innovations": ["core innovations", "contributions", "novelty"],
        "datasets": ["datasets", "data sets"],
        "experimental_parameters": ["experimental", "experiments", "setup", "parameters", "methodology", "approach"],
        "results": ["results", "evaluation"],
        "limitations": ["limitations", "discussions", "future work"],
    }

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        low = line.lower()
        found = None
        for key, aliases in synonyms.items():
            for alias in aliases:
                if low.startswith(alias) or f" {alias}" in low or low == alias:
                    found = key
                    break
            if found:
                break
        if found:
            current = found
            continue
        if current:
            blocks[current].append(line)

    core_innovations = "\n".join(blocks["core_innovations"]).strip()
    datasets = "\n".join(blocks["datasets"]).strip()
    experimental_parameters = "\n".join(blocks["experimental_parameters"]).strip()
    results = "\n".join(blocks["results"]).strip()
    limitations = "\n".join(blocks["limitations"]).strip()

    # Generate a lightweight analysis summary
    summaries = []
    if core_innovations:
        summaries.append("核心创新: 我们提取的要点包括 {}".format(core_innovations[:200]))
    if datasets:
        summaries.append("数据集: {}".format(datasets[:200]))
    if experimental_parameters:
        summaries.append("实验参数: {}".format(experimental_parameters[:200]))
    if results:
        summaries.append("结果: {}".format(results[:200]))
    if limitations:
        summaries.append("局限性: {}".format(limitations[:200]))
    analysis_summary = " | ".join(summaries)

    return {
        "core_innovations": core_innovations,
        "datasets": datasets,
        "experimental_parameters": experimental_parameters,
        "results": results,
        "limitations": limitations,
        "analysis_summary": analysis_summary,
    }
