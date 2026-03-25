"""语音前端论文速递 - 主入口"""

import argparse
import json
import os
import shutil
import glob
from datetime import datetime

from arxiv_fetcher import fetch_arxiv_papers
from evaluator import evaluate_paper
from filter import assign_category, filter_papers
from html_generator import generate_html
from paper_detail import fetch_paper_details


def load_run_state(state_path: str) -> dict:
    """Load incremental run state from JSON. Returns {"papers": []} when missing or invalid."""
    if not state_path:
        return {"papers": []}
    try:
        if os.path.exists(state_path):
            with open(state_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            papers = data.get("papers", []) if isinstance(data, dict) else []
            return {"papers": papers}
    except Exception:
        pass
    return {"papers": []}


def save_run_state(state_path: str, papers_list: list) -> None:
    """Save incremental run state to JSON."""
    try:
        os.makedirs(os.path.dirname(state_path), exist_ok=True)
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump({"papers": papers_list}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ 无法保存运行状态(state): {e}")


def main():
    parser = argparse.ArgumentParser(description="语音前端论文速递")
    parser.add_argument("--max-papers", type=int, help="最大论文数", default=20)
    parser.add_argument("--output", type=str, help="输出路径", default=None)
    parser.add_argument("--api-key", type=str, help="OpenAI API Key", default=None)
    args = parser.parse_args()

    target_date = datetime.now()

    # Determine output directory and ensure it exists
    output_dir = os.path.join(os.path.dirname(__file__), "tmp")
    os.makedirs(output_dir, exist_ok=True)
    # New feature: compute paths for state tracking and HTML output
    state_path = os.path.join(output_dir, "speech_run_state.json")

    # Determine latest HTML cache to support fallback when there are no new papers
    latest_html = None
    html_pattern = os.path.join(output_dir, "speech_daily_*.html")
    candidates = glob.glob(html_pattern)
    if candidates:
        latest_html = max(candidates, key=lambda p: os.path.getmtime(p))

    # Load historical run state
    prev_state = load_run_state(state_path)
    prev_papers = prev_state.get("papers", []) or []
    prev_ids = {p.get("arxiv_id") for p in prev_papers if p.get("arxiv_id")}

    # Attempt incremental analysis with new papers only
    print("📥 获取最新论文...")
    papers = fetch_arxiv_papers()
    print(f"   获取到 {len(papers)} 篇论文")

    print("🔍 过滤音频前端相关论文...")
    papers = filter_papers(papers)
    papers = papers[: args.max_papers]
    print(f"   过滤后剩余 {len(papers)} 篇")

    new_candidates = [p for p in papers if p.get("arxiv_id") not in prev_ids]
    allowed_new = max(0, len(papers) == 0 and 0 or (args.max_papers - len(prev_papers)))
    new_papers = new_candidates[:allowed_new]

    if new_papers:
        print(f"✨ 发现 {len(new_papers)} 篇新文献，将仅对新文献进行分析...")
        for i, paper in enumerate(new_papers):
            print(f"   [{i + 1}/{len(new_papers)}] {paper['arxiv_id']}")
            details = fetch_paper_details(paper["arxiv_id"])
            paper.update(details)
            paper["category"] = assign_category(paper)

        api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
        if api_key:
            print("🤖 LLM 评价论文...")
            for i, paper in enumerate(new_papers):
                print(f"   [{i + 1}/{len(new_papers)}] 评价 {paper['arxiv_id']}")
                eval_result = evaluate_paper(paper, api_key)
                paper.update(eval_result)
        else:
            print("⚠️ 未设置 OPENAI_API_KEY，跳过 LLM 评价")

        # Merge with previously analyzed papers and deduplicate by arxiv_id
        merged_papers = prev_papers + new_papers
        seen = set()
        deduped = []
        for p in merged_papers:
            aid = p.get("arxiv_id")
            if aid and (aid not in seen):
                deduped.append(p)
                seen.add(aid)

        html_content = generate_html(deduped, target_date)
        if not args.output:
            today_html = os.path.join(output_dir, f"speech_daily_{target_date.strftime('%Y%m%d')}.html")
        else:
            today_html = args.output

        with open(today_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ 完成！输出: {today_html}")
        # Save updated run state
        save_run_state(state_path, deduped)
        return today_html
    else:
        # No new papers. Try reuse latest HTML cache if available
        if latest_html:
            today_html = os.path.join(output_dir, f"speech_daily_{target_date.strftime('%Y%m%d')}.html")
            try:
                shutil.copy2(latest_html, today_html)
                print(f"✨ 无新文献，复用最近缓存，输出到：{today_html}")
                return today_html
            except Exception as e:
                print(f"⚠️ 无法拷贝最近缓存：{e}")
        # Fallback: 进行一次完整分析以确保产出
        print("📥 重新执行完整分析以确保产出...")
        print("📥 获取最新论文...")
        papers = fetch_arxiv_papers()
        print(f"   获取到 {len(papers)} 篇论文")
        print("🔍 过滤音频前端相关论文...")
        papers = filter_papers(papers)
        papers = papers[: args.max_papers]
        print(f"   过滤后剩余 {len(papers)} 篇")

        print("📖 获取论文详情...")
        for i, paper in enumerate(papers):
            print(f"   [{i + 1}/{len(papers)}] {paper['arxiv_id']}")
            details = fetch_paper_details(paper["arxiv_id"])
            paper.update(details)
            paper["category"] = assign_category(paper)

        api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
        if api_key:
            print("🤖 LLM 评价论文...")
            for i, paper in enumerate(papers):
                print(f"   [{i + 1}/{len(papers)}] 评价 {paper['arxiv_id']}")
                eval_result = evaluate_paper(paper, api_key)
                paper.update(eval_result)
        else:
            print("⚠️ 未设置 OPENAI_API_KEY，跳过 LLM 评价")

        print("🎨 生成 HTML...")
        html_content = generate_html(papers, target_date)

        output_path = args.output
        if not output_path:
            output_path = os.path.join(output_dir, f"speech_daily_{target_date.strftime('%Y%m%d')}.html")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ 完成！输出: {output_path}")
        # Save state for future incremental runs
        save_run_state(state_path, papers)
        return output_path
    # (End of incremental/fallback flow)


if __name__ == "__main__":
    main()
