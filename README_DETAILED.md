# Detailed README: Speech Front-end Daily

This document expands the main README with deeper guidance for installation, operation, architecture, workflows, and governance aligned with the doc-driven AGENTS.md expectations.

Table of Contents
- Overview
- Quick Start
- Advanced Usage
- Architecture & Data Flow
- CLI & Configuration
- Output Format
- Testing & Quality
- Documentation & Roadmap
- Troubleshooting
- Contributing
- License

1. Overview
- Purpose: automatic arXiv fetch, filter for audio-front-end papers, read/parse data, evaluate with LLM, and render an HTML report.
- Scope: papers in speech enhancement, noise suppression, beamforming, DOA, AEC, and related audio front-end topics.

2. Quick Start (baseline)
- Prereqs: Python 3.10+, OpenSSH (for SSH-based workflows if used), git.
- Install: 
  pip install -e .
- API keys: export OPENAI_API_KEY=...
- Run: 
  python -X utf8 -m src.main --api-key YOUR_API_KEY --max-papers 8
- Output: src/tmp/speech_daily_YYYYMMDD.html

3. Advanced Usage
- Use --date to fetch historical data.
- Use --output to place reports in custom location.
- Use --max-papers to cap the number of papers processed.
- Use --log-level for verbose debugging.

4. Architecture & Data Flow
- Modules: arxiv_fetcher, filter, paper_detail, html_generator, evaluator, main, quick_start.
- Data flow: arxiv fetch -> filter -> detail -> categorize -> evaluate -> render HTML.

5. CLI & Configuration
- api-key: OpenAI/OpenRouter key; if using OpenRouter, pass sk-or-; otherwise OpenAI key.
- max-papers: number of papers to process after filtering.
- output: HTML output path.
- date: historical fetch date (YYYY-MM-DD) if provided.

6. Output Format
- HTML cards per paper with sections: 简介、技术方案、实验结果、结论、工程价值、评分等.

7. Testing & Quality
- Lint: ruff check src/; tests: pytest.
- Commit messages should follow Conventional Commits.

8. Documentation & Roadmap
- See BACKLOG.md, CHECKLIST.md, CHANGELOG.md, RELEASE-NOTE.md for doc-driven planning.
- Roadmap: extend to include multi-dataset evaluation and CI integration.

9. Troubleshooting
- ARXIV 404: Occurs when date refers to future data; ensure dates are real.
- SSH: ensure SSH key is registered with GitHub for push access.
- OpenAI/OpenRouter: ensure API key has proper permissions and quotas.

10. Contributing & License
- Contributions are welcome. See LICENSE for license terms.
