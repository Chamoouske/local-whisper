from __future__ import annotations

import argparse
import sys
from pathlib import Path

from local_whisper.files import collect_videos, existing_subtitle
from local_whisper.transcriber import _is_cuda_error, load_model, transcribe_file


def main():
    parser = argparse.ArgumentParser(description="Gera legendas .srt em pt-BR a partir de vídeos")
    parser.add_argument("paths", nargs="+", help="Vídeo(s) ou pasta(s) com vídeos")
    parser.add_argument("-o", "--output", help="Diretório de saída (padrão: mesmo do vídeo)")
    parser.add_argument("-d", "--device", choices=["cuda", "cpu", "auto"], default="auto",
                        help="Dispositivo (padrão: auto — tenta GPU, fallback CPU)")
    parser.add_argument("--force", action="store_true",
                        help="Transcreve mesmo que já exista uma legenda")
    args = parser.parse_args()

    videos = collect_videos(args.paths)
    if not videos:
        print("Nenhum vídeo encontrado.")
        sys.exit(1)

    output_dir = Path(args.output) if args.output else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    if not args.force:
        extra = [output_dir] if output_dir else None
        filtered: list[Path] = []
        for v in videos:
            sub = existing_subtitle(v, extra)
            if sub:
                print(f"[=] pulando {v.name} — já tem legenda ({sub.name})")
            else:
                filtered.append(v)
        videos = filtered

    if not videos:
        print("\n[✓] Nada a fazer — todos os vídeos já têm legenda")
        return

    print(f"[*] {len(videos)} vídeo(s) para transcrever")
    model, device = load_model(args.device)
    print(f"[*] Modelo: small | Dispositivo: {device}\n")

    for i, video in enumerate(videos, start=1):
        try:
            transcribe_file(model, video, output_dir, index=i, total=len(videos))
        except Exception as e:
            if device == "cuda" and _is_cuda_error(e):
                print(f"    ⚠ Erro CUDA — recarregando modelo na CPU")
                model, device = load_model("cpu")
                transcribe_file(model, video, output_dir)
            else:
                print(f"    ✗ erro: {e}")

    print("\n[✓] Concluído")
