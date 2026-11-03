from __future__ import annotations

import os
import sys
import time
from pathlib import Path

MODEL_SIZE = "small"

CUDA_ERRORS = ("cublas", "cudnn", "cuda", "out of memory", "nvrtc", "cufft")


def _is_cuda_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(k in msg for k in CUDA_ERRORS)


def _add_cuda12_to_path() -> None:
    """Procura CUDA 12.x instalado e adiciona ao PATH/DLL search antes de importar ctranslate2."""
    base = Path(os.environ.get("CUDA_PATH", r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA"))
    if base.name.startswith("v"):
        candidates = [base]
    else:
        candidates = sorted(base.glob("v12.*"), reverse=True)

    for cuda_dir in candidates:
        bin_dir = cuda_dir / "bin"
        cublas = bin_dir / "cublas64_12.dll"
        if cublas.exists():
            os.environ["PATH"] = str(bin_dir) + os.pathsep + os.environ.get("PATH", "")
            if sys.platform == "win32":
                os.add_dll_directory(str(bin_dir))
            return


_add_cuda12_to_path()

import ctranslate2  # noqa: E402
from faster_whisper import WhisperModel  # noqa: E402
from tqdm import tqdm  # noqa: E402

from local_whisper.srt import segments_to_srt  # noqa: E402


def _try_cuda() -> WhisperModel | None:
    try:
        if ctranslate2.get_cuda_device_count() == 0:
            return None
        model = WhisperModel(MODEL_SIZE, device="cuda", compute_type="float16")
        return model
    except Exception as e:
        reason = str(e).split("\n")[0]
        print(f"[!] GPU indisponível — {reason}")
        return None


def load_model(device: str | None = None) -> tuple[WhisperModel, str]:
    if device and device != "auto":
        compute = "float16" if device == "cuda" else "int8"
        return WhisperModel(MODEL_SIZE, device=device, compute_type=compute), device

    model = _try_cuda()
    if model:
        return model, "cuda"

    print("[!] Usando CPU")
    return WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8"), "cpu"


def _fmt_duration(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def transcribe_file(model: WhisperModel, video: Path, output_dir: Path | None,
                    index: int = 0, total: int = 0) -> Path:
    dest = (output_dir or video.parent) / (video.stem + ".srt")
    batch = f" ({index}/{total})" if total else ""
    print(f"  → {video.name}{batch}")

    start = time.perf_counter()
    segments_gen, info = model.transcribe(
        str(video),
        language="pt",
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )

    duration = info.duration
    collected = []
    bar = tqdm(
        total=int(duration),
        unit="s",
        bar_format="    {l_bar}{bar}| {n_fmt}/{total_fmt}s [{elapsed}<{remaining}]",
        leave=False,
    )
    prev_end = 0.0
    for seg in segments_gen:
        collected.append(seg)
        delta = seg.end - prev_end
        if delta > 0:
            bar.update(int(delta))
            prev_end = seg.end
    bar.update(bar.total - bar.n)
    bar.close()

    elapsed = time.perf_counter() - start
    srt = segments_to_srt(collected)

    if not collected:
        print(f"    ⚠ nenhuma fala detectada ({elapsed:.1f}s)")
        return dest

    dest.write_text(srt, encoding="utf-8")
    print(f"    ✓ {len(collected)} segmentos — {elapsed:.1f}s → {dest.name}")
    return dest
