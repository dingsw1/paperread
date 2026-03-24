"""LLM 评价模块"""

import json
import os
import re
from typing import Any

import requests


SYSTEM_PROMPT = """你是一位音频前端领域的资深专家（语音增强、降噪、波束形成、DOA、AEC、去混响、目标说话人提取等）。请根据论文全文，给出专业、客观、中肯的评价。

请严格按照以下JSON格式输出，不要输出其他内容：
{
  "summary": "论文简介（一句话概括解决什么问题+核心贡献）",
  "innovation": "核心创新（与现有方法的本质区别，50字以内）",
  "architecture": "模型架构简述（网络结构、输入输出，80字以内）",
  "training": "训练策略（loss设计、数据增强，60字以内）",
  "datasets": "使用的数据集名称",
  "baseline": "对比的baseline方法（至少1个）",
  "results": {
    "PESQ": "具体数值或提升幅度，如: 2.45→3.12 (+0.67)",
    "STOI": "具体数值或提升幅度",
    "SI_SDR": "具体数值或提升幅度",
    "DNSMOS": "具体数值",
    "other": "其他指标"
  },
  "sota_claim": "论文是否声称SOTA（是/否/未明确）",
  "score": 分数(0-10),
  "reason": "评分理由（必须包含：创新性、实验充分性、工程价值，100字以内）",
  "engineering_value": "工程落地价值评估（高/中/低）",
  "concerns": "潜在问题或局限性（如有）"
}"""


def is_openrouter_key(key: str) -> bool:
    """检查是否是 OpenRouter 的 key"""
    return key.startswith("sk-or-")


def evaluate_paper(paper: dict[str, Any], api_key: str | None = None) -> dict[str, Any]:
    """使用 LLM 评价论文

    Args:
        paper: 论文信息
        api_key: API Key (支持 OpenAI 和 OpenRouter)

    Returns:
        评价结果
    """
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        return {
            "innovation": "未配置 API Key",
            "architecture": "N/A",
            "training": "N/A",
            "metrics": "N/A",
            "datasets": "N/A",
            "score": 0,
            "reason": "请设置 OPENAI_API_KEY 环境变量",
            "engineering_value": "未知",
        }

    title = paper.get("title", "")
    abstract = paper.get("abstract", "")
    arxiv_id = paper.get("arxiv_id", "")
    full_content = paper.get("full_content", "")

    user_prompt = f"""arXiv ID: {arxiv_id}
标题: {title}
摘要: {abstract}"""

    if full_content:
        user_prompt += f"""

论文全文（摘录）:
{full_content}"""

    user_prompt += """

请基于以上内容，分析并给出专业评价。"""

    try:
        if is_openrouter_key(api_key):
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://speech-daily.local",
                "X-Title": "Speech Front-end Daily",
            }
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": "deepseek/deepseek-chat",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1000,
                },
                timeout=60,
            )

            if resp.status_code != 200:
                return {
                    "summary": "论文简介",
                    "innovation": f"API错误: {resp.status_code}",
                    "architecture": "N/A",
                    "training": "N/A",
                    "datasets": "N/A",
                    "baseline": "N/A",
                    "results": {},
                    "sota_claim": "未明确",
                    "score": 0,
                    "reason": f"OpenRouter错误: {resp.text[:100]}",
                    "engineering_value": "未知",
                    "concerns": "",
                }

            result = resp.json()
            content = result["choices"][0]["message"]["content"]
        else:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}],
                temperature=0.3,
                max_tokens=1500,
            )
            content = response.choices[0].message.content

        if content:
            try:
                json_match = re.search(r"\{[\s\S]*\}", content)
                if json_match:
                    result = json.loads(json_match.group())
                    return result
            except json.JSONDecodeError:
                pass
    except Exception as e:
        return {
            "summary": "论文简介",
            "innovation": f"调用失败: {str(e)[:30]}",
            "architecture": "N/A",
            "training": "N/A",
            "datasets": "N/A",
            "baseline": "N/A",
            "results": {},
            "sota_claim": "未明确",
            "score": 0,
            "reason": f"LLM 调用失败: {str(e)[:50]}",
            "engineering_value": "未知",
            "concerns": "",
        }

    return {
        "summary": "论文简介",
        "innovation": "解析失败",
        "architecture": "N/A",
        "training": "N/A",
        "datasets": "N/A",
        "baseline": "N/A",
        "results": {},
        "sota_claim": "未明确",
        "score": 0,
        "reason": "无法解析 LLM 输出",
        "engineering_value": "未知",
        "concerns": "",
    }
