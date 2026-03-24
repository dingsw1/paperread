"""论文精读模块 - 获取和解析论文详情"""

import re
from typing import Any

import requests
from bs4 import BeautifulSoup


METRICS_PATTERN = re.compile(r"(PESQ|STOI|SDR|SI-SDR|SAR|SIR|SNR)[^\d]*([\d.]+)", re.IGNORECASE)
DATASET_PATTERN = re.compile(
    r"(LibriSpeech|VCTK|WSJ0|WSJ1|CHiME|VoxCeleb|DNS|Interspeech|ICASSP|ICASS|AVSpeech|Noisyspeech)", re.IGNORECASE
)
SECTIONS_PATTERN = re.compile(
    r"(introduction|related work|method|methodology|model|approach|experimental|experiments|results|conclusion)",
    re.IGNORECASE,
)


def fetch_paper_details(arxiv_id: str) -> dict[str, Any]:
    """获取论文详情

    Args:
        arxiv_id: 论文 ID

    Returns:
        论文详情字典
    """
    paper: dict[str, Any] = {"arxiv_id": arxiv_id}

    abs_url = f"https://arxiv.org/abs/{arxiv_id}v1"
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}v1.pdf"
    html_url = f"https://arxiv.org/html/{arxiv_id}v1"

    paper["abs_url"] = abs_url
    paper["pdf_url"] = pdf_url
    paper["html_url"] = html_url

    try:
        resp = requests.get(abs_url, timeout=30)
        if resp.status_code == 200:
            details = parse_abs_page(resp.text, arxiv_id)
            paper.update(details)
    except Exception:
        pass

    try:
        resp = requests.get(html_url, timeout=30)
        if resp.status_code == 200:
            full_content = extract_full_content(resp.text)
            if full_content:
                paper["full_content"] = full_content
    except Exception:
        pass

    return paper


def extract_full_content(html: str, max_chars: int = 40000) -> str:
    """提取论文全文内容（截取关键章节）

    Args:
        html: HTML 内容
        max_chars: 最大字符数

    Returns:
        提取的论文内容
    """
    soup = BeautifulSoup(html, "lxml")

    content_parts = []

    for tag in soup.find_all(["h1", "h2", "h3", "h4", "p"]):
        text = tag.get_text(strip=True)
        if len(text) < 20:
            continue

        if tag.name in ["h1", "h2", "h3"]:
            content_parts.append(f"\n## {text}\n")
        else:
            content_parts.append(text)

    full_text = " ".join(content_parts)

    if len(full_text) > max_chars:
        full_text = full_text[:max_chars] + "\n\n[内容已截断...]"

    return full_text


def extract_abstract_from_content(content: str) -> str:
    """从全文内容中提取摘要"""
    content = content.strip()

    parts = content.split("##")
    if parts and len(parts[0]) > 50:
        first_part = parts[0].strip()
        if len(first_part) > 100:
            return first_part[:1000]

    lines = [line.strip() for line in content.split("\n") if line.strip()]
    for i, line in enumerate(lines):
        if line.startswith("Abstract"):
            for j in range(i + 1, min(i + 10, len(lines))):
                if len(lines[j]) > 100:
                    return lines[j][:1000]

    return ""


def parse_abs_page(html: str, arxiv_id: str) -> dict[str, Any]:
    """解析摘要页面"""
    soup = BeautifulSoup(html, "lxml")

    details: dict[str, Any] = {}

    title_elem = soup.select_one("h1.title")
    if title_elem:
        details["title"] = title_elem.get_text(strip=True).replace("Title:", "").strip()

    abstract_elem = soup.select_one("div.abstract")
    if abstract_elem:
        abstract = abstract_elem.get_text(strip=True).replace("Abstract:", "").strip()
        details["abstract"] = abstract

        metrics = METRICS_PATTERN.findall(abstract)
        if metrics:
            details["metrics"] = ", ".join([f"{m[0]}: {m[1]}" for m in metrics])

        datasets = DATASET_PATTERN.findall(abstract)
        if datasets:
            details["datasets"] = list(set(datasets))

    authors: list[str] = []
    for author in soup.select("div.authors a"):
        authors.append(author.get_text(strip=True))
    if authors:
        details["authors"] = authors

    comments_elem = soup.select_one("div.comments")
    if comments_elem:
        details["comments"] = comments_elem.get_text(strip=True)

        if "code" in details["comments"].lower() or "github" in details["comments"].lower():
            code_match = re.search(r"(https?://github\.com/[^\s]+)", details["comments"])
            if code_match:
                details["code"] = code_match.group(1)

    subjects = []
    for sub in soup.select("div.subjects a"):
        subjects.append(sub.get_text(strip=True))
    if subjects:
        details["subjects"] = subjects

    return details


def parse_html_details(html: str, arxiv_id: str) -> dict[str, Any]:
    """解析 HTML 页面获取论文详情"""
    soup = BeautifulSoup(html, "lxml")

    details: dict[str, Any] = {}

    title_elem = soup.select_one("h1.title")
    details["title"] = str(title_elem.get_text(strip=True).replace("Title:", "").strip()) if title_elem else ""

    abstract_elem = soup.select_one("div.abstract")
    if abstract_elem:
        details["abstract"] = str(abstract_elem.get_text(strip=True).replace("Abstract:", "").strip())

    authors: list[str] = []
    for author in soup.select("div.authors a"):
        authors.append(str(author.get_text(strip=True)))
    details["authors"] = authors

    comments_elem = soup.select_one("div.comments")
    if comments_elem:
        details["comments"] = str(comments_elem.get_text(strip=True).replace("Comments:", "").strip())

    code_elem = soup.select_one("a[href*=github]")
    if code_elem:
        details["code"] = str(code_elem.get("href") or "")

    demo_elem = soup.select("a.link-other")
    demos: list[str] = []
    for link in demo_elem:
        href = str(link.get("href") or "")
        if "demo" in href.lower() or "audio" in href.lower():
            demos.append(href)
    if demos:
        details["demos"] = demos

    subjects: list[str] = []
    for sub in soup.select("div.subjects a"):
        subjects.append(str(sub.get_text(strip=True)))
    details["subjects"] = subjects

    return details
