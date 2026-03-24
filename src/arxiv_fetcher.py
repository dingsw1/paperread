"""arXiv 论文获取模块"""
import re

import requests
from bs4 import BeautifulSoup


def fetch_arxiv_papers(max_papers: int = 200) -> list[dict]:
    """获取近期的 arXiv 音频前端相关论文
    
    Args:
        max_papers: 最大获取论文数
    
    Returns:
        论文列表
    """
    papers: list[dict] = []
    base_url = "https://arxiv.org/list"
    
    for category in ["cs.SD", "eess.AS"]:
        url = f"{base_url}/{category}/recent"
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "lxml")
            
            for dt in soup.find_all("dt"):
                link = dt.select_one("a[href*='/abs/']")
                if not link:
                    continue
                    
                href = str(link.get("href") or "")
                arxiv_id = href.split("/abs/")[-1].strip()
                
                dd = dt.find_next_sibling("dd")
                if not dd:
                    continue
                
                title_elem = dd.select_one("div.list-title")
                title = title_elem.get_text(strip=True).replace("Title: ", "") if title_elem else ""
                
                authors_elem = dd.select_one("div.list-authors")
                authors = authors_elem.get_text(strip=True).replace("Authors: ", "") if authors_elem else ""
                
                date_match = re.search(r"(\d{1,2} \w{3} \d{4})", dd.get_text())
                date_str = date_match.group(1) if date_match else ""
                
                papers.append({
                    "arxiv_id": arxiv_id,
                    "title": title,
                    "authors": authors,
                    "category": category,
                    "date": date_str,
                })
        except Exception:
            pass
    
    papers = deduplicate_papers(papers)
    return papers[:max_papers]


def deduplicate_papers(papers: list[dict]) -> list[dict]:
    """合并去重"""
    seen = set()
    result = []
    for p in papers:
        arxiv_id = p["arxiv_id"].split("v")[0]
        if arxiv_id not in seen:
            seen.add(arxiv_id)
            p["arxiv_id"] = arxiv_id
            result.append(p)
    return result
