"""HTML 生成模块"""

import html
from datetime import datetime


CATEGORY_COLORS = {
    "Beamforming": "#7C3AED",
    "Speech Enhancement": "#059669",
    "Noise Suppression": "#DC2626",
    "AEC": "#EA580C",
    "DOA": "#0891B2",
    "Dereverberation": "#4F46E5",
    "Target Speaker Extraction": "#BE185D",
    "Speech Separation": "#854D0E",
    "Other": "#6B7280",
}


def generate_html(papers: list[dict], date: datetime) -> str:
    """生成 HTML 网页日报

    Args:
        papers: 论文列表
        date: 日期

    Returns:
        HTML 字符串
    """
    categories: dict[str, int] = {}
    for paper in papers:
        cat = paper.get("category", "Other")
        categories[cat] = categories.get(cat, 0) + 1

    html_parts = [
        """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>语音前端论文速递</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #1a1a2e;
            color: #e5e5e5;
            line-height: 1.6;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { 
            font-size: 1.8rem; 
            margin-bottom: 20px; 
            color: #fff;
            text-align: center;
        }
        .overview {
            background: #16213e;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
        }
        .overview h2 {
            font-size: 1.2rem;
            margin-bottom: 15px;
            color: #fff;
        }
        .stats {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 20px;
        }
        .stat-item {
            background: #0f3460;
            padding: 10px 20px;
            border-radius: 8px;
        }
        .stat-label { color: #94a3b8; font-size: 0.9rem; }
        .stat-value { color: #fff; font-size: 1.5rem; font-weight: bold; }
        .category-stats {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .category-tag {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
        }
        .category-block {
            margin-bottom: 30px;
        }
        .category-title {
            font-size: 1.3rem;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid;
        }
        .paper-card {
            background: #16213e;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }
        .paper-header {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-bottom: 10px;
        }
        .paper-title {
            font-size: 1.1rem;
            color: #fff;
            flex: 1;
        }
        .paper-title a {
            color: inherit;
            text-decoration: none;
        }
        .paper-title a:hover {
            color: #60a5fa;
        }
        .tag {
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: 500;
            white-space: nowrap;
        }
        .paper-meta {
            font-size: 0.85rem;
            color: #94a3b8;
            margin: 8px 0;
        }
        .paper-meta span { margin-right: 15px; }
        .abstract {
            background: #0f3460;
            padding: 12px;
            border-radius: 8px;
            margin: 10px 0;
            font-size: 0.9rem;
        }
        details {
            margin-top: 10px;
        }
        summary {
            cursor: pointer;
            color: #60a5fa;
            font-size: 0.9rem;
        }
        .tech-content {
            background: #0f3460;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            font-size: 0.9rem;
        }
        .tech-content h4 {
            color: #fff;
            margin: 10px 0 5px;
        }
        .tech-content ul {
            margin-left: 20px;
            color: #cbd5e1;
        }
        .results { margin-top: 10px; padding: 10px; background: #0f3460; border-radius: 8px; }
        .results span { display: inline-block; margin-right: 15px; color: #94a3b8; font-size: 0.85rem; }
        .sota { margin-top: 10px; font-size: 0.9rem; }
        .concerns { margin-top: 10px; padding: 10px; background: #3d1f1f; border-radius: 8px; font-size: 0.85rem; color: #fca5a5; }
        .reason { margin-top: 10px; padding: 10px; background: #1e3a5f; border-radius: 8px; font-size: 0.9rem; }
        .engineering { margin-top: 10px; font-size: 0.9rem; }
        .score { font-size: 1.2rem; font-weight: bold; color: #fbbf24; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎙️ 语音前端论文速递"""
    ]

    html_parts.append(f'<p style="color:#94a3b8;margin-top:10px;">📅 {date.strftime("%Y-%m-%d")}</p>')
    html_parts.append("""</h1>""")

    html_parts.append("""<div class="overview">
            <h2>📊 概览</h2>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">""")
    html_parts.append(str(len(papers)))
    html_parts.append("""</div>
                    <div class="stat-label">论文总数</div>
                </div>
            </div>
            <div class="category-stats">""")

    for cat, count in sorted(categories.items()):
        color = CATEGORY_COLORS.get(cat, "#6B7280")
        html_parts.append(f'<span class="category-tag" style="background:{color}">{cat}: {count}</span>')

    html_parts.append("""</div>
        </div>""")

    grouped: dict[str, list[dict]] = {}
    for paper in papers:
        cat = paper.get("category", "Other")
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(paper)

    for cat in CATEGORY_COLORS:
        if cat not in grouped:
            continue
        cat_papers = grouped[cat]
        color = CATEGORY_COLORS[cat]

        html_parts.append(
            f'<div class="category-block"><h2 class="category-title" style="border-color:{color}">🎯 {cat}</h2>'
        )

        for i, paper in enumerate(cat_papers, 1):
            html_parts.append(generate_paper_card(paper, i, cat))

        html_parts.append("</div>")

    html_parts.append("""</div>
</body>
</html>""")

    return "".join(html_parts)


def generate_paper_card(paper: dict, index: int, category: str) -> str:
    """生成单个论文卡片"""
    color = CATEGORY_COLORS.get(category, "#6B7280")

    title = html.escape(paper.get("title", ""))
    arxiv_id = paper.get("arxiv_id", "")
    authors = paper.get("authors", [])
    if isinstance(authors, str):
        authors = [authors]
    authors_str = html.escape(", ".join(authors[:5]) + ("..." if len(authors) > 5 else ""))
    abs_url = paper.get("abs_url", f"https://arxiv.org/abs/{arxiv_id}")
    pdf_url = paper.get("pdf_url", f"https://arxiv.org/pdf/{arxiv_id}.pdf")
    code = paper.get("code", "")
    score = paper.get("score", 0)
    innovation = html.escape(paper.get("innovation", ""))
    architecture = html.escape(paper.get("architecture", ""))
    training = html.escape(paper.get("training", ""))
    datasets = html.escape(paper.get("datasets", ""))
    baseline = html.escape(paper.get("baseline", ""))
    results = paper.get("results", {})
    sota_claim = html.escape(paper.get("sota_claim", ""))
    concerns = html.escape(paper.get("concerns", ""))
    reason = html.escape(paper.get("reason", ""))
    engineering_value = html.escape(paper.get("engineering_value", ""))
    summary = html.escape(paper.get("summary", ""))

    card = f'''<div class="paper-card">
            <div class="paper-header">
                <h3 class="paper-title"><a href="{abs_url}" target="_blank">{index}. {title}</a></h3>
                <span class="tag" style="background:{color}">{category}</span>
            </div>
            <div class="paper-meta">
                <span>📄 <a href="{abs_url}" target="_blank">{arxiv_id}</a></span>
                <span>📑 <a href="{pdf_url}" target="_blank">PDF</a></span>'''

    if code:
        card += f''' <span>💻 <a href="{code}" target="_blank">Code</a></span>'''

    card += f"""</div>
            <div class="paper-meta"><span>👥 {authors_str}</span></div>"""

    if summary:
        card += f"""
            <div class="abstract"><b>简介：</b>{summary}</div>"""

    if innovation or architecture:
        card += """
            <details>
                <summary>🔧 技术方案</summary>
                <div class="tech-content">"""
        if innovation:
            card += f"""
                    <h4>💡 核心创新</h4>
                    <p>{innovation}</p>"""
        if architecture:
            card += f"""
                    <h4>🏗️ 模型架构</h4>
                    <p>{architecture}</p>"""
        if training:
            card += f"""
                    <h4>🎯 训练策略</h4>
                    <p>{training}</p>"""
        if datasets:
            card += f"""
                    <h4>📊 数据集</h4>
                    <p>{datasets}</p>"""
        if baseline:
            card += f"""
                    <h4>📈 Baseline对比</h4>
                    <p>{baseline}</p>"""
        card += """
                </div>
            </details>"""

    if results:
        results_html = ""
        for k, v in results.items():
            if v:
                results_html += f"<span>{k}: {v}</span> "
        if results_html:
            card += f"""
            <div class="results"><span>📊 实验结果：</span>{results_html}</div>"""

    if sota_claim and sota_claim != "未明确":
        sota_color = "#10B981" if sota_claim == "是" else "#6B7280"
        card += f"""
            <div class="sota"><span>🏆 SOTA声明：</span><span style="color:{sota_color}">{sota_claim}</span></div>"""

    if concerns:
        card += f"""
            <div class="concerns"><span>⚠️ 潜在问题：</span>{concerns}</div>"""

    if reason:
        card += f"""
            <div class="reason"><b>💭 评价：</b>{reason}</div>"""

    if engineering_value:
        value_color = {"高": "#10B981", "中": "#F59E0B", "低": "#EF4444"}.get(engineering_value, "#6B7280")
        card += f"""
            <div class="engineering"><span>🔧 工程价值：</span><span style="color:{value_color}">{engineering_value}</span></div>"""

    card += f"""
            <p class="score">⭐ {score}/10</p>
        </div>"""

    return card
