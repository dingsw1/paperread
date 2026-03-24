Speech Front-end Daily — Paper Digest

A lightweight toolset to fetch recent audio-front-end papers from arXiv, filter for relevance,
read key parts, run a (ltm) evaluation, and generate an HTML report for quick browsing.

Key features:
- Pulls arXiv lists for cs.SD/new and eess.AS/new
- Filters for true audio front-end papers (with beamforming now context-checked)
- Reads abstracts (and optionally full text) and extracts structured data
- LLM-based evaluation of papers (configurable models)
- Outputs a clean HTML report: src/tmp/speech_daily_YYYYMMDD.html

Current status: 8 filtered papers are produced in the latest run. Beamforming papers are filtered
to ensure audio-domain relevance only when an audio context is detected.

Note: All code is ASCII for portability. The project uses a small, opinionated subset of the arXiv
and LLM workflows to keep costs predictable during exploration.

-----------------------------------------------------------------

Getting Started
- Prerequisites: Python 3.10+, Git
- Install dependencies (editable):
  $ pip install -e .
- Configure API keys (one of the following):
  - OpenAI: export OPENAI_API_KEY=your_key
  - OpenRouter: use an OpenRouter key; the code will auto-detect if your key starts with sk-or-
- Run the main workflow:
  python -X utf8 -m src.main --api-key YOUR_API_KEY --max-papers 20

Output
- HTML report: src/tmp/speech_daily_YYYYMMDD.html
- The report includes summary, experiment results, and an optional LLM-based evaluation
- You can open the file directly in a browser for review

Minimal Quick Start Script
- A small helper is provided to run an end-to-end quick demo and produce the HTML output
- See scripts/quick_start.py for details

Contributing
- Run lint and tests locally:
  $ ruff check src/ --fix
  $ pytest -q
- Please prefix commits with conventional commits style and provide changelog entries as needed

License
- MIT

Contact
- For questions, reach out to the repo maintainers
