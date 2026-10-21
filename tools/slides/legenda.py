# -*- coding: utf-8 -*-
"""Queima legendas curtas num vídeo do dono (faixa inferior, no estilo do formato A).

    python3 tools/slides/legenda.py ENTRADA.mp4 SAIDA.mp4 "0-3.8:texto" "3.8-7.8:outro [[destaque]]" ...

O vídeo original não é alterado; sai um arquivo novo com o mesmo áudio.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from render import chrome, md  # noqa: E402

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%dpx;height:%dpx;background:transparent;overflow:hidden}
.band{position:absolute;left:0;right:0;bottom:0;padding:%dpx %dpx %dpx 64px;
  background:linear-gradient(180deg,rgba(11,31,58,0) 0%%,rgba(11,31,58,.8) 30%%,rgba(11,31,58,.85) 100%%)}
p{font-family:'Montserrat';font-weight:800;color:#fff;font-size:%dpx;line-height:1.22}
.hl{background:#F7C700;color:#0B1F3A;padding:0 .12em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.h{font-family:'Montserrat';font-weight:700;color:rgba(255,255,255,.7);font-size:%dpx;letter-spacing:.1em;margin-top:%dpx}
"""


def size(video: str) -> tuple[int, int]:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                          "-of", "json", video], capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    return s["width"], s["height"]


def overlay_png(text: str, w: int, h: int, out: Path) -> None:
    k = w / 1080
    fonts = (HERE / "fonts" / "fonts.css").read_text().replace("url('", "url('" + (HERE / "fonts").as_uri() + "/")
    css = CSS % (w, h, 200 * k, 160 * k, 430 * k, 62 * k, 26 * k, 24 * k)  # acima da faixa que o Instagram cobre
    page = (f"<!doctype html><html><head><meta charset='utf-8'><style>{fonts}{css}</style></head><body>"
            f"<div class='band'><p>{md(text)}</p><div class='h'>@ANOVA.AUTISMO</div></div></body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(page)
    subprocess.run([chrome(), "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--default-background-color=00000000", f"--window-size={w},{h}", "--virtual-time-budget=3000",
                    f"--screenshot={out}", Path(f.name).as_uri()], check=True, capture_output=True, timeout=120)
    Path(f.name).unlink()


def main() -> None:
    src, dst, *cues = sys.argv[1:]
    w, h = size(src)
    tmp = Path(tempfile.mkdtemp())
    args, chain, last = ["ffmpeg", "-v", "error", "-y", "-i", src], [], "0:v"
    for i, cue in enumerate(cues, 1):
        span, text = cue.split(":", 1)
        a, b = span.split("-")
        png = tmp / f"o{i}.png"
        overlay_png(text, w, h, png)
        args += ["-i", str(png)]
        chain.append(f"[{last}][{i}:v]overlay=0:0:enable='between(t,{a},{b})'[v{i}]")
        last = f"v{i}"
    args += ["-filter_complex", ";".join(chain), "-map", f"[{last}]", "-map", "0:a?", "-c:v", "libx264",
             "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", dst]
    subprocess.run(args, check=True)


if __name__ == "__main__":
    main()
