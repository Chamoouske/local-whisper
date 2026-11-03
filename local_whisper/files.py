from __future__ import annotations

from pathlib import Path

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".m4v", ".ts"}

SUBTITLE_EXTENSIONS = {
    ".srt", ".vtt", ".ass", ".ssa", ".sub", ".sbv",
    ".ttml", ".dfxp", ".smi", ".stl", ".usf", ".idx",
}


def collect_videos(paths: list[str]) -> list[Path]:
    videos: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            videos.extend(sorted(f for f in path.iterdir() if f.suffix.lower() in VIDEO_EXTENSIONS))
        elif path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS:
            videos.append(path)
        else:
            print(f"[!] ignorando: {p}")
    return videos


def existing_subtitle(video: Path, extra_dirs: list[Path] | None = None) -> Path | None:
    dirs = [video.parent]
    if extra_dirs:
        dirs.extend(d for d in extra_dirs if d != video.parent)
    for d in dirs:
        for ext in SUBTITLE_EXTENSIONS:
            candidate = d / (video.stem + ext)
            if candidate.exists():
                return candidate
    return None
