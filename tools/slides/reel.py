# -*- coding: utf-8 -*-
"""Transforma um carrossel já renderizado num reel 1080x1920 (slides com zoom lento e transição).

    python3 tools/slides/reel.py 56 57 60      # grava media/anova.autismo/video_<slug>.mp4 (+ .txt e .jpg)

O reel sai sem música: áudio com direitos não entra aqui. Quem quiser trilha
adiciona no Instagram ao republicar, ou troca o arquivo.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from posts import POSTS  # noqa: E402

MEDIA = HERE.parent.parent / "media" / "anova.autismo"
BG = {"dsm": "0xFFFFFF", "foto": "0x0B1F3A", "conheca": "0xFFF6EC"}
SECS, FADE, FPS = 5.0, 0.6, 30


def build(p: dict, out_dir: Path) -> Path:
    folder = out_dir / f"post-{p['n']:02d}-{p['slug']}"
    slides = sorted(folder.glob("slide-*.png"))
    if len(slides) != 5:
        sys.exit(f"{folder.name}: renderize os slides antes (render.py {p['n']})")
    bg = BG[p["format"]]
    frames = int(SECS * FPS)
    args = ["ffmpeg", "-v", "error", "-y"]
    total = len(slides) * SECS - (len(slides) - 1) * FADE
    for s in slides:  # uma imagem só por entrada: o zoompan gera os quadros do slide
        args += ["-i", str(s)]
    args += ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo"]
    chains = []
    for i in range(len(slides)):
        chains.append(
            f"[{i}]scale=1080:1350,zoompan=z='1+0.035*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":d={frames}:s=1080x1350:fps={FPS},pad=1080:1920:0:285:color={bg},format=yuv420p,setsar=1[v{i}]")
    last, offset = "v0", SECS - FADE
    for i in range(1, len(slides)):
        chains.append(f"[{last}][v{i}]xfade=transition=fade:duration={FADE}:offset={offset:.2f}[x{i}]")
        last, offset = f"x{i}", offset + SECS - FADE
    out = out_dir / f"video_{p['slug'].replace('-', '_')}.mp4"
    args += ["-filter_complex", ";".join(chains), "-map", f"[{last}]", "-map", f"{len(slides)}:a",
             "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-profile:v", "high", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", str(out)]
    subprocess.run(args, check=True)
    (out.with_suffix(".txt")).write_text((folder / "caption.txt").read_text(encoding="utf-8"), encoding="utf-8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(slides[0]), "-vf",
                    f"pad=1080:1920:0:285:color={bg}", "-q:v", "3", str(out.with_suffix(".jpg"))], check=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("only", nargs="+", type=int)
    ap.add_argument("--out", default=str(MEDIA))
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg não encontrado")
    for p in POSTS:
        if p["n"] in a.only:
            print(build(p, Path(a.out)).name)


if __name__ == "__main__":
    main()
