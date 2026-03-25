import json
import os
import sys
from datetime import datetime

import pytest

# Ensure the repository root is on sys.path so that `import src.main` works
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import src.main as main_module


@pytest.fixture(autouse=True)
def clean_tmp_dir():
    tmp_dir = os.path.join(os.path.dirname(main_module.__file__), "tmp")
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir, exist_ok=True)
    # remove any existing files before each test
    for fname in os.listdir(tmp_dir):
        fpath = os.path.join(tmp_dir, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)
    yield
    # cleanup after test
    for fname in os.listdir(tmp_dir):
        fpath = os.path.join(tmp_dir, fname)
        if os.path.isfile(fpath):
            os.remove(fpath)


def test_full_run_creates_output_and_state(monkeypatch):
    today = datetime.now().strftime("%Y%m%d")
    tmp_dir = os.path.join(os.path.dirname(main_module.__file__), "tmp")

    captured = {}

    def fake_generate_html(papers, date):
        captured["papers"] = papers
        captured["date"] = date
        return "<html>mock</html>"

    # Patch dependencies to simulate a simple single-paper run
    monkeypatch.setattr(main_module, "fetch_arxiv_papers", lambda: [{"arxiv_id": "A1"}])
    monkeypatch.setattr(main_module, "filter_papers", lambda papers: papers)
    monkeypatch.setattr(
        main_module,
        "fetch_paper_details",
        lambda arxiv_id: {"arxiv_id": arxiv_id, "title": "Alpha", "abs_url": f"https://arxiv.org/abs/{arxiv_id}"},
    )
    monkeypatch.setattr(main_module, "assign_category", lambda p: "Other")
    monkeypatch.setattr(main_module, "evaluate_paper", lambda paper, key: {"score": 9})
    monkeypatch.setattr(main_module, "generate_html", fake_generate_html)

    sys_argv_backup = sys.argv
    sys.argv = ["prog", "--api-key", "dummy", "--max-papers", "20"]
    try:
        main_module.main()
    finally:
        sys.argv = sys_argv_backup

    output_file = os.path.join(tmp_dir, f"speech_daily_{today}.html")
    assert os.path.exists(output_file)
    with open(output_file, "r", encoding="utf-8") as f:
        data = f.read()
    assert "<html>mock</html>" in data

    state_path = os.path.join(tmp_dir, "speech_run_state.json")
    assert os.path.exists(state_path)
    with open(state_path, "r", encoding="utf-8") as f:
        s = json.load(f)
    assert "papers" in s and len(s["papers"]) == 1
    assert s["papers"][0]["arxiv_id"] == "A1"
    # ensure incremental papers were captured by generate_html
    assert captured.get("papers") is not None


def test_incremental_with_new_paper(monkeypatch):
    today = datetime.now().strftime("%Y%m%d")
    tmp_dir = os.path.join(os.path.dirname(main_module.__file__), "tmp")
    state_path = os.path.join(tmp_dir, "speech_run_state.json")
    os.makedirs(tmp_dir, exist_ok=True)
    # Preload previous state with A1
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump({"papers": [{"arxiv_id": "A1", "title": "Alpha"}]}, f)

    captured = {}

    def fake_generate_html(papers, date):
        captured["papers"] = papers
        return "<html>mock</html>"

    # New papers: A1 (existing) and A2 (new)
    monkeypatch.setattr(main_module, "fetch_arxiv_papers", lambda: [{"arxiv_id": "A1"}, {"arxiv_id": "A2"}])
    monkeypatch.setattr(main_module, "filter_papers", lambda papers: papers)

    def fake_details(arxiv_id):
        return {"arxiv_id": arxiv_id, "title": f"Title {arxiv_id}", "abs_url": f"https://arxiv.org/abs/{arxiv_id}"}

    monkeypatch.setattr(main_module, "fetch_paper_details", fake_details)
    monkeypatch.setattr(main_module, "assign_category", lambda p: "Other")
    monkeypatch.setattr(main_module, "evaluate_paper", lambda paper, key: {"score": 7})
    monkeypatch.setattr(main_module, "generate_html", fake_generate_html)

    import sys

    sys_argv_backup = sys.argv
    sys.argv = ["prog", "--api-key", "dummy", "--max-papers", "20"]
    try:
        main_module.main()
    finally:
        sys.argv = sys_argv_backup

    # state should contain A1 and A2
    with open(state_path, "r", encoding="utf-8") as f:
        s = json.load(f)
    ids = {p["arxiv_id"] for p in s["papers"]}
    assert {"A1", "A2"}.issubset(ids)
    # ensure HTML was generated with 2 papers
    assert len(captured.get("papers", [])) == 2


def test_no_new_papers_uses_latest_cache(monkeypatch):
    tmp_dir = os.path.join(os.path.dirname(main_module.__file__), "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    # Create a cached latest HTML with an old timestamp
    cached_path = os.path.join(tmp_dir, "speech_daily_20000101.html")
    with open(cached_path, "w", encoding="utf-8") as f:
        f.write("<html>cache</html>")
    old_ts = datetime(2000, 1, 1).timestamp()
    os.utime(cached_path, (old_ts, old_ts))

    # Preload a state with A1 so no new papers are produced
    state_path = os.path.join(tmp_dir, "speech_run_state.json")
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump({"papers": [{"arxiv_id": "A1"}]}, f)

    # arxiv_papers returns A1 so new_papers will be empty
    monkeypatch.setattr(main_module, "fetch_arxiv_papers", lambda: [{"arxiv_id": "A1"}])
    monkeypatch.setattr(main_module, "filter_papers", lambda papers: papers)
    monkeypatch.setattr(main_module, "fetch_paper_details", lambda arxiv_id: {"arxiv_id": arxiv_id, "title": "A1"})
    monkeypatch.setattr(main_module, "assign_category", lambda p: "Other")
    # Do not perform HTML generation to force cache usage path
    monkeypatch.setattr(main_module, "generate_html", lambda papers, date: "<html>mock</html>")

    import sys

    old_argv = sys.argv
    sys.argv = ["prog", "--max-papers", "20"]
    try:
        main_module.main()
    finally:
        sys.argv = old_argv

    today = datetime.now().strftime("%Y%m%d")
    today_html = os.path.join(tmp_dir, f"speech_daily_{today}.html")
    assert os.path.exists(today_html)
    with open(today_html, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "<html>cache</html>"
