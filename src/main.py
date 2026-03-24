"""语音前端论文速递 - 主入口"""

import argparse
import os
from datetime import datetime

from arxiv_fetcher import fetch_arxiv_papers
from evaluator import evaluate_paper
from filter import assign_category, filter_papers
from html_generator import generate_html
from paper_detail import fetch_paper_details


def main():
    parser = argparse.ArgumentParser(description="语音前端论文速递")
    parser.add_argument("--max-papers", type=int, help="最大论文数", default=20)
    parser.add_argument("--output", type=str, help="输出路径", default=None)
    parser.add_argument("--api-key", type=str, help="OpenAI API Key", default=None)
    args = parser.parse_args()

    target_date = datetime.now()

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
        output_dir = os.path.join(os.path.dirname(__file__), "tmp")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"speech_daily_{target_date.strftime('%Y%m%d')}.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ 完成！输出: {output_path}")

    return output_path


if __name__ == "__main__":
    main()
