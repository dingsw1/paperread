"""论文过滤模块"""

KEYWORDS_INCLUDE = [
    "speech enhancement",
    "noise suppression",
    "beamforming",
    "microphone array",
    "sound source localization",
    "doa",
    "direction of arrival",
    "acoustic echo cancellation",
    "aec",
    "dereverberation",
    "howling suppression",
    "target speaker extraction",
    "speaker extraction",
    "speech separation",
    "source separation",
    "noise reduction",
    "speech denoising",
    "acoustic beamforming",
    "mvdr",
    "music separation",
    "audio source separation",
    "voice activity detection",
    "vad",
    "acoustic noise",
]

# Extra guard for beamforming papers to ensure audio-domain relevance
AUDIO_CONTEXT_KEYWORDS = [
    "audio",
    "speech",
    "microphone",
    "signal processing",
    "speech enhancement",
    "front-end",
]


def _has_audio_context(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in AUDIO_CONTEXT_KEYWORDS)


KEYWORDS_EXCLUDE = [
    "automatic speech recognition",
    "speech recognition",
    "text to speech",
    "speech synthesis",
    "large language model",
    "gpt-",
    "video-to-audio",
    "v2a",
    "foley",
    "music generation",
    "music synthesis",
    "speaker verification",
    "speaker identification",
    "emotion recognition",
    "voice conversion",
]


def filter_papers(papers: list[dict]) -> list[dict]:
    """过滤论文，只保留音频前端相关"""
    filtered = []
    for paper in papers:
        if is_audio_front_end(paper):
            filtered.append(paper)
    return filtered


def is_audio_front_end(paper: dict) -> bool:
    """判断论文是否属于音频前端"""
    title = paper.get("title", "").lower()
    authors = paper.get("authors", "").lower()
    combined = f"{title} {authors}"

    for kw in KEYWORDS_EXCLUDE:
        if kw in combined:
            return False

    # Special handling: if the paper mentions beamforming, require audio context
    if "beamforming" in combined:
        if not _has_audio_context(combined):
            return False

    for kw in KEYWORDS_INCLUDE:
        if kw in combined:
            return True

    return False


def assign_category(paper: dict) -> str:
    """为论文分配方向类别"""
    title = paper.get("title", "").lower()

    if any(kw in title for kw in ["beamforming", "microphone array", "mvdr", "acoustic beamforming"]):
        return "Beamforming"
    if "speech enhancement" in title or "speech denoising" in title:
        return "Speech Enhancement"
    if "noise" in title or "denoising" in title:
        return "Noise Suppression"
    if "echo" in title or "aec" in title:
        return "AEC"
    if "doa" in title or "localization" in title or "direction of arrival" in title:
        return "DOA"
    if "dereverberation" in title:
        return "Dereverberation"
    if "target speaker" in title or "speaker extraction" in title:
        return "Target Speaker Extraction"
    if "separation" in title:
        return "Speech Separation"

    return "Other"
