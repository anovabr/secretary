# -*- coding: utf-8 -*-
"""Renderiza os carrosséis de posts.py em PNG 1080x1350, mais um story 1080x1920 por post.

    python3 tools/slides/render.py              # todos, para media/anova.autismo/
    python3 tools/slides/render.py 56 57        # só esses
    python3 tools/slides/render.py --out DIR    # para outra pasta (prévia)

Cada slide é uma página HTML (fontes e imagens locais, em tools/slides/) fotografada
pelo Chrome headless do Playwright. Nada sai da máquina.
"""

from __future__ import annotations

import argparse
import glob
import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
from posts import POSTS  # noqa: E402

W, H = 1080, 1350
HANDLE = "anova.autismo"
URL = "autismo.anovasaude.org"


def chrome() -> str:
    found = sorted(glob.glob(os.path.expanduser(
        "~/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell")))
    if not found:
        sys.exit("chrome-headless-shell não encontrado (npx playwright install chromium-headless-shell)")
    return found[-1]


def md(text: str) -> str:
    """**negrito** e [[destaque]] sobre texto escapado."""
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\[\[(.+?)\]\]", r'<span class="hl">\1</span>', t)
    return t


def asset(name: str) -> str:
    return (HERE / "assets" / name).as_uri()


def dots(i: int, n: int = 5) -> str:
    return '<div class="dots">' + "".join(
        f'<i class="{"on" if k == i else ""}"></i>' for k in range(n)) + "</div>"


ARROW = ('<svg class="arrow" viewBox="0 0 120 20" preserveAspectRatio="xMaxYMid meet"><path d="M0 10 H112 M100 2 L114 10 L100 18" '
         'fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:%dpx;height:%dpx;overflow:hidden}
body{position:relative;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
.dots{display:flex;gap:14px}
.dots i{width:18px;height:18px;border-radius:50%%;display:block}
.arrow{width:110px;height:20px;display:inline-block;vertical-align:middle}
""" % (W, H)

DSM_CSS = """
body{background:#fff;font-family:'Lato';color:#1E1E24;padding:0 72px}
.hdr{display:flex;align-items:center;height:205px;border-bottom:2.5px solid #1E1E24;padding-top:20px}
.hdr img{height:96px;margin-right:24px}
.hdr .brand{font-size:36px;color:#6B6B70;flex:1}
.hdr .k{font-weight:700;color:#C9A227;font-size:25px;letter-spacing:.2em;text-transform:uppercase}
.lbl{font-weight:700;font-size:23px;letter-spacing:.16em;text-transform:uppercase}
.gold{color:#C9A227}
.cover .lbl{margin-top:64px}
.cover h1{font-weight:900;font-size:88px;line-height:1.06;letter-spacing:-.01em;margin-top:20px}
.cover .bottom{position:absolute;left:72px;right:72px;top:930px;border-top:1.5px solid #ddd;padding-top:36px}
.cover .lead{font-size:40px;color:#6B6B70}
.cover .punch{font-size:40px;font-weight:900;margin-top:10px;line-height:1.25}
.manual{padding:40px 0 34px;border-bottom:1.5px solid #1E1E24}
.manual p{font-style:italic;color:#6B6B70;font-size:32px;line-height:1.35;margin-top:12px}
.real{padding-top:34px}
.real .item{font-weight:700;font-size:35px;line-height:1.38;padding:24px 0;border-bottom:1.5px solid #e4e4e4}
.note{position:absolute;left:72px;right:72px;top:1060px;font-size:30px;line-height:1.4;color:#1E1E24}
.foot{position:absolute;left:72px;right:72px;bottom:118px;display:flex;justify-content:space-between;align-items:center}
.foot .ref{font-style:italic;font-size:21px;color:#6B6B70}
.foot .go{font-weight:700;font-size:23px;letter-spacing:.16em;color:#C9A227}
.foot .go .arrow{width:40px;height:16px;margin-left:12px}
body>.dots{position:absolute;left:72px;bottom:62px}
.dots i{background:#ddd}.dots i.on{background:#C9A227}
.cta .logo{margin-top:70px;height:205px}
.cta .ask{font-size:40px;color:#6B6B70;margin-top:80px}
.cta h2{font-weight:900;font-size:76px;margin-top:12px;letter-spacing:-.01em}
.cta .btn{display:inline-block;margin-top:36px;background:#C9A227;color:#1E1E24;font-weight:900;font-size:30px;
  letter-spacing:.06em;padding:22px 42px;border-radius:60px}
.cta .two{position:absolute;left:72px;right:72px;top:1000px;display:flex;border-top:1.5px solid #ddd;padding-top:30px}
.cta .two div{flex:1;padding-right:24px}
.cta .two div+div{border-left:1.5px solid #ddd;padding-left:28px}
.cta .two p{font-size:28px;line-height:1.35;margin-top:10px;color:#1E1E24}
"""

FOTO_CSS = """
body{background:#0B1F3A;font-family:'Montserrat';color:#fff}
.hl{background:#F7C700;color:#0B1F3A;padding:0 .14em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.chip{position:absolute;top:56px;left:64px;background:#fff;border-radius:22px;padding:12px 22px 12px 14px;display:flex;align-items:center;gap:14px}
.chip img{height:58px}.chip span{font-weight:700;font-size:24px;color:#0B1F3A;letter-spacing:.02em}
.art{position:absolute;inset:0}
.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,31,58,0) 30%,rgba(11,31,58,.92) 62%,#0B1F3A 78%)}
.cover .txt{position:absolute;left:64px;right:64px;top:820px}
.cover .pre{font-weight:900;font-size:66px;line-height:1.08;text-transform:uppercase;letter-spacing:-.01em}
.cover .big{font-weight:900;font-size:76px;line-height:1.12;text-transform:uppercase;margin-top:10px;letter-spacing:-.01em}
.cover .sub{font-weight:500;font-size:30px;line-height:1.4;text-transform:uppercase;margin-top:30px;letter-spacing:.02em;color:#E8EDF5}
.cover .sub b{font-weight:800;color:#fff}
.bar{position:absolute;left:64px;right:64px;bottom:60px;display:flex;justify-content:space-between;align-items:center;
  font-weight:600;font-size:24px;letter-spacing:.08em;color:rgba(255,255,255,.75);text-transform:uppercase}
.bar .arrow{width:120px;color:#fff}
.top{position:absolute;left:64px;right:64px;top:70px;display:flex;justify-content:space-between;font-weight:800;font-size:26px;letter-spacing:.16em;text-transform:uppercase}
.top .k{color:#F7C700}.top .n{color:rgba(255,255,255,.5)}
.body .main{position:absolute;left:64px;right:64px;top:300px;font-weight:800;font-size:66px;line-height:1.24;letter-spacing:-.01em}
.body .more{position:absolute;left:64px;right:110px;top:840px;font-weight:500;font-size:36px;line-height:1.45;color:#D5DDEA;
  border-left:6px solid #F7C700;padding-left:30px}
.ref{position:absolute;left:64px;right:64px;bottom:140px;font-weight:500;font-size:21px;color:rgba(255,255,255,.55)}
.cta .main{position:absolute;left:64px;right:64px;top:300px;font-weight:900;font-size:78px;line-height:1.16;letter-spacing:-.01em}
.cta .btn{position:absolute;left:64px;top:650px;background:#F7C700;color:#0B1F3A;font-weight:900;font-size:36px;padding:26px 46px;border-radius:70px}
.cta .small{position:absolute;left:64px;top:790px;font-weight:600;font-size:28px;color:#D5DDEA}
.cta .nd{position:absolute;left:64px;right:64px;top:930px;font-weight:600;font-size:28px;line-height:1.4;color:rgba(255,255,255,.7);
  border-top:1.5px solid rgba(255,255,255,.2);padding-top:30px}
.cta .logo{position:absolute;right:64px;bottom:130px;background:#fff;border-radius:24px;padding:18px 26px}
.cta .logo img{height:110px;display:block}
"""

CONHECA_CSS = """
body{background:#FFF6EC;font-family:'Nunito';color:#1E1E24}
.blob{position:absolute;border-radius:50%;filter:blur(2px)}
.hl{color:#E5366B}
.cover .hdr{position:absolute;top:58px;left:64px;display:flex;align-items:center;gap:14px;font-weight:800;font-size:26px;color:#4a4a55}
.cover .hdr img{height:62px}
.lines{position:absolute;left:0;right:0;top:220px;display:flex;flex-direction:column;align-items:center;gap:22px}
.pill{font-family:'Baloo 2';font-weight:800;font-size:138px;line-height:1.02;padding:18px 54px 4px;border-radius:48px;letter-spacing:-.01em}
.pill.plain{background:#fff;color:#1E1E24;box-shadow:0 10px 0 rgba(30,30,36,.08)}
.pill.pink{background:#E5366B;color:#fff;box-shadow:0 10px 0 #B8204F}
.pill.blue{background:#2E6FD9;color:#fff;box-shadow:0 10px 0 #1C4FA6}
.cover .sub{margin:26px 110px 0;text-align:center;font-weight:800;font-size:42px;line-height:1.35;color:#4a4a55}
.people{position:absolute;left:0;right:0;bottom:120px;display:flex;justify-content:center;gap:10px}
.people img{width:236px;height:236px}
.deco{position:absolute}
.bar{position:absolute;left:64px;right:64px;bottom:52px;display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:25px;color:#6B6B70}
.bar .arrow{width:90px;color:#E5366B}
.top{position:absolute;left:64px;right:64px;top:64px;display:flex;justify-content:space-between;align-items:center}
.tag{font-weight:800;font-size:26px;letter-spacing:.06em;text-transform:uppercase;background:#2E6FD9;color:#fff;padding:10px 24px;border-radius:40px}
.top .n{font-weight:800;font-size:26px;color:#9a9aa3}
.body .emo{position:absolute;left:64px;top:230px;width:230px;height:230px}
.body h2{position:absolute;left:64px;right:64px;top:520px;font-family:'Baloo 2';font-weight:800;font-size:108px;line-height:1.02;letter-spacing:-.01em}
.body p{position:absolute;left:64px;right:80px;top:820px;font-weight:700;font-size:46px;line-height:1.42;color:#33333b}
.body .ref{position:absolute;left:64px;right:64px;bottom:122px;font-weight:700;font-size:22px;color:#8a8a93}
.cta .emo{position:absolute;left:50%;transform:translateX(-50%);top:150px;width:250px;height:250px}
.cta .lead{position:absolute;left:0;right:0;top:450px;text-align:center;font-weight:800;font-size:44px;color:#4a4a55}
.cta h2{position:absolute;left:60px;right:60px;top:525px;text-align:center;font-family:'Baloo 2';font-weight:800;font-size:96px;line-height:1.02}
.cta .btn{position:absolute;left:50%;transform:translateX(-50%);top:780px;white-space:nowrap;background:#E5366B;color:#fff;font-family:'Baloo 2';
  font-weight:800;font-size:46px;padding:20px 56px 12px;border-radius:60px;box-shadow:0 10px 0 #B8204F}
.cta .small{position:absolute;left:0;right:0;top:930px;text-align:center;font-weight:700;font-size:30px;color:#6B6B70}
.cta .nd{position:absolute;left:0;right:0;top:1010px;text-align:center;font-weight:800;font-size:28px;color:#4a4a55}
.cta .logo{position:absolute;left:50%;transform:translateX(-50%);bottom:110px;height:120px}
"""

STORY_CSS = """
html,body{width:1080px;height:1920px}
body{display:flex;flex-direction:column;align-items:center}
.st-top{margin-top:150px;font-weight:900;font-size:44px;letter-spacing:.18em;text-transform:uppercase;padding:16px 40px;border-radius:60px}
.st-card{margin-top:60px;width:860px;height:1075px;border-radius:36px;box-shadow:0 30px 80px rgba(0,0,0,.28);overflow:hidden}
.st-card img{width:100%;height:100%;display:block}
.st-bot{margin-top:70px;font-weight:800;font-size:40px;text-align:center;line-height:1.4}
.st-handle{margin-top:18px;font-weight:700;font-size:32px;opacity:.7}
"""


def page(css: str, body: str, cls: str = "", size=(W, H)) -> str:
    fonts = (HERE / "fonts" / "fonts.css").read_text().replace("url('", "url('" + (HERE / "fonts").as_uri() + "/")
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{fonts}{BASE_CSS}{css}"
            f"html,body{{width:{size[0]}px;height:{size[1]}px}}</style></head>"
            f"<body class='{cls}'>{body}</body></html>")


# ---------------------------------------------------------------------------
# Formato dsm — série "DSM-5 na vida real", como o post 39
# ---------------------------------------------------------------------------

def dsm_header(i: int, label: str) -> str:
    return (f'<div class="hdr"><img src="{asset("logo-a.png")}"><div class="brand">ANOVA Autismo</div>'
            f'<div class="k">{label} · {i + 1:02d}</div></div>')


def dsm_slides(p: dict) -> list[str]:
    c, ref = p["cover"], html.escape(p["ref"])
    foot = lambda go="ARRASTE": f'<div class="foot"><span class="ref">{ref}</span><span class="go">{go}{ARROW}</span></div>'
    out = [page(DSM_CSS, dsm_header(0, "DSM-5 na vida real")
                + f'<div class="lbl gold">{md(c["kicker"])}</div><h1>{md(c["title"])}</h1>'
                + f'<div class="bottom"><div class="lead">{md(c["lead"])}</div><div class="punch">{md(c["punch"])}</div></div>'
                + foot() + dots(0), "cover")]
    for k, ex in enumerate(p["examples"]):
        items = "".join(f'<div class="item">{md(r)}</div>' for r in ex["real"])
        out.append(page(DSM_CSS, dsm_header(k + 1, f"Exemplo {k + 1}")
                        + f'<div class="manual"><div class="lbl">No manual</div><p>{md(ex["manual"])}</p></div>'
                        + f'<div class="real"><div class="lbl gold">Na vida real</div>{items}</div>'
                        + f'<div class="note">{md(ex["note"])}</div>' + foot() + dots(k + 1)))
    t = p["cta"]
    out.append(page(DSM_CSS, dsm_header(4, "Próximo passo")
                    + f'<img class="logo" src="{asset("logo-full.png")}">'
                    + '<div class="ask">Se reconheceu em mais de um exemplo?</div><h2>Faça o teste gratuito</h2>'
                    + '<div class="btn">TOQUE NO LINK DA BIO</div>'
                    + f'<div class="two"><div><div class="lbl gold">Comente</div><p>{md(t["comment"])}</p></div>'
                    + f'<div><div class="lbl gold">Lembre</div><p>{md(t["remember"])}</p></div></div>'
                    + f'<div class="foot"><span class="ref">{URL} · não substitui diagnóstico</span>'
                    + f'<span class="go">LINK NA BIO{ARROW}</span></div>' + dots(4), "cta"))
    return out


# ---------------------------------------------------------------------------
# Formato foto (A) — "Precisamos falar"
# ---------------------------------------------------------------------------

def motif(kind: str) -> str:
    """Ilustração do topo da capa quando não há foto: traço amarelo e branco sobre o azul."""
    grid = "".join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#ffffff" opacity=".12"/>'
                   for x in range(40, 1080, 56) for y in range(40, 900, 56))
    if kind == "wave":  # meltdown à esquerda, shutdown (linha reta) à direita
        import math
        pts = []
        for x in range(0, 600, 6):
            a = 30 + 260 * (x / 600) ** 1.6
            pts.append(f"{x},{430 + a * math.sin(x / 9.0) * math.cos(x / 23.0):.1f}")
        art = (f'<polyline points="{" ".join(pts)}" fill="none" stroke="#F7C700" stroke-width="7" stroke-linejoin="round"/>'
               f'<line x1="600" y1="430" x2="1080" y2="430" stroke="#fff" stroke-width="7" opacity=".85"/>'
               f'<circle cx="600" cy="430" r="16" fill="#fff"/>')
    elif kind == "loading":  # barra parada no começo
        art = ('<rect x="140" y="370" width="800" height="90" rx="45" fill="none" stroke="#fff" stroke-width="7" opacity=".9"/>'
               '<rect x="160" y="390" width="118" height="50" rx="25" fill="#F7C700"/>'
               '<text x="140" y="560" fill="#fff" opacity=".8" font-family="Montserrat" font-weight="700" font-size="44" '
               'letter-spacing="6">CARREGANDO… 12%</text>'
               + "".join(f'<circle cx="{820 + 46 * k}" cy="250" r="12" fill="#F7C700" opacity="{.3 + .25 * k}"/>' for k in range(3)))
    else:  # pulse — batimento e ondas do corpo
        pts = "0,430 330,430 380,430 410,330 450,560 495,240 535,470 565,430 1080,430"
        art = (''.join(f'<circle cx="540" cy="430" r="{r}" fill="none" stroke="#fff" stroke-width="3" opacity="{o}"/>'
                       for r, o in ((150, .35), (250, .22), (360, .12)))
               + f'<polyline points="{pts}" fill="none" stroke="#F7C700" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>')
    return f'<svg class="art" viewBox="0 0 1080 1350" preserveAspectRatio="xMidYMin slice">{grid}{art}</svg>'


def foto_slides(p: dict) -> list[str]:
    c, ref = p["cover"], html.escape(p["ref"])
    chip = f'<div class="chip"><img src="{asset("logo-a.png")}"><span>ANOVA Autismo</span></div>'
    bar = f'<div class="bar"><span>@{HANDLE}</span>{ARROW}</div>'
    photo = p.get("photo")
    art = (f'<img class="art" style="width:100%;height:100%;object-fit:cover" src="{(HERE / "assets" / photo).as_uri()}">'
           if photo else motif(p.get("motif", "pulse")))
    out = [page(FOTO_CSS, art + '<div class="shade"></div>' + chip
                + f'<div class="txt"><div class="pre">{md(c["pre"])}</div><div class="big"><span class="hl">{md(c["hl"])}</span></div>'
                + f'<div class="sub">{md(c["sub"])}</div></div>' + bar, "cover")]
    for k, b in enumerate(p["body"]):
        out.append(page(FOTO_CSS, f'<div class="top"><span class="k">{md(b["kicker"])}</span><span class="n">{k + 2}/5</span></div>'
                        + f'<div class="main">{md(b["text"])}</div><div class="more">{md(b["more"])}</div>'
                        + f'<div class="ref">{ref}</div>' + bar, "body"))
    t = p["cta"]
    out.append(page(FOTO_CSS, '<div class="top"><span class="k">E agora?</span><span class="n">5/5</span></div>'
                    + f'<div class="main">{md(t["lead"])}<br><span class="hl">{md(t["hl"])}</span></div>'
                    + '<div class="btn">Gratuito · link na bio</div>'
                    + '<div class="small">8 minutos · sem cadastro · resultado na hora</div>'
                    + f'<div class="nd">Rastreio não é diagnóstico: o resultado orienta a busca por uma avaliação profissional.</div>'
                    + f'<div class="logo"><img src="{asset("logo-full.png")}"></div>'
                    + f'<div class="bar"><span>{URL}</span><span></span></div>', "cta"))
    return out


# ---------------------------------------------------------------------------
# Formato conheca (B) — perguntas
# ---------------------------------------------------------------------------

def blobs(seed: int, strong: bool) -> str:
    spots = [(-160, -120, 520, "#FFD6E0"), (720, -60, 460, "#D6E9FF"), (-120, 980, 480, "#CDEFE3"),
             (760, 900, 520, "#FFE7B8"), (820, 470, 260, "#FFD6E0"), (40, 560, 200, "#D6E9FF")]
    spots = spots[seed % 2:] + spots[:seed % 2]
    keep = spots if strong else spots[:3]
    out = "".join(f'<div class="blob" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c};opacity:{.95 if strong else .7}"></div>'
                  for x, y, s, c in keep)
    # rabiscos e símbolo do infinito no lugar das peças de quebra-cabeça
    out += ('<svg class="deco" style="left:0;top:0" width="1080" height="1350">'
            '<path d="M120 200 q30 -40 60 0 t60 0" stroke="#2E6FD9" stroke-width="7" fill="none" stroke-linecap="round"/>'
            '<path d="M930 860 l22 -36 M960 880 l40 -10 M935 910 l30 26" stroke="#E5366B" stroke-width="7" stroke-linecap="round"/>'
            '<path d="M1000 760 a26 26 0 1 1 0.1 0" stroke="#F28C28" stroke-width="7" fill="none"/>'
            '</svg>' if strong else "")
    return out


def conheca_slides(p: dict) -> list[str]:
    c = p["cover"]
    bar = f'<div class="bar"><span>@{HANDLE}</span><span>arraste {ARROW}</span></div>'
    lines = "".join(f'<div class="pill {style}" style="font-size:{min(138, 1550 // len(t))}px">{md(t)}</div>'
                    for t, style in c["lines"])
    people = "".join(f'<img src="{asset("emoji-" + e + ".png")}">' for e in c["people"])
    out = [page(CONHECA_CSS, blobs(p["n"], True)
                + f'<div class="hdr"><img src="{asset("logo-a-alpha.png")}">ANOVA Autismo</div>'
                + f'<img class="deco" style="right:70px;top:150px;width:120px" src="{asset("emoji-light_bulb.png")}">'
                + f'<img class="deco" style="left:70px;top:800px;width:92px" src="{asset("emoji-infinity.png")}">'
                + f'<div class="lines">{lines}<div class="sub">{md(c["sub"])}</div></div>'
                + f'<div class="people">{people}</div>' + bar, "cover")]
    colors = ["#2E6FD9", "#E5366B", "#3BA55D"]
    for k, b in enumerate(p["body"]):
        out.append(page(CONHECA_CSS, blobs(p["n"] + k + 1, False)
                        + f'<div class="top"><span class="tag" style="background:{colors[k]}">{md(b["kicker"])}</span><span class="n">{k + 2}/5</span></div>'
                        + f'<img class="emo" src="{asset("emoji-" + b["emoji"] + ".png")}">'
                        + f'<h2>{md(b["head"])}</h2><p>{md(b["text"])}</p>'
                        + f'<div class="ref">{html.escape(b["ref"])}</div>' + bar, "body"))
    t = p["cta"]
    out.append(page(CONHECA_CSS, blobs(p["n"], True)
                    + f'<img class="emo" src="{asset("emoji-waving_hand-medium.png")}">'
                    + f'<div class="lead">{md(t["lead"])}</div><h2>{md(t["head"])}</h2>'
                    + '<div class="btn">Toque no link da bio</div>'
                    + '<div class="small">8 minutos · sem cadastro · resultado na hora</div>'
                    + '<div class="nd">Rastreio não é diagnóstico.</div>'
                    + f'<img class="logo" src="{asset("logo-full-alpha.png")}">'
                    + f'<div class="bar"><span>{URL}</span><span>5/5</span></div>', "cta"))
    return out


def story(p: dict, cover_png: Path) -> str:
    theme = {"dsm": ("#FFFFFF", "#1E1E24", "#C9A227", "#1E1E24", "'Lato'"),
             "foto": ("#0B1F3A", "#FFFFFF", "#F7C700", "#0B1F3A", "'Montserrat'"),
             "conheca": ("#FFF6EC", "#1E1E24", "#E5366B", "#FFFFFF", "'Nunito'")}[p["format"]]
    bg, fg, accent, on_accent, font = theme
    body = (f'<div class="st-top" style="background:{accent};color:{on_accent}">Post novo</div>'
            f'<div class="st-card"><img src="{cover_png.as_uri()}"></div>'
            f'<div class="st-bot">Arraste o carrossel no perfil</div><div class="st-handle">@{HANDLE}</div>')
    return page(STORY_CSS + f"body{{background:{bg};color:{fg};font-family:{font}}}", body, size=(1080, 1920))


# ---------------------------------------------------------------------------

def shoot(html_text: str, out: Path, size=(W, H)) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html_text)
        src = f.name
    try:
        subprocess.run([chrome(), "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--window-size={size[0]},{size[1]}", "--virtual-time-budget=4000",
                        f"--screenshot={out}", Path(src).as_uri()],
                       check=True, capture_output=True, timeout=120)
    finally:
        os.unlink(src)


BUILD = {"dsm": dsm_slides, "foto": foto_slides, "conheca": conheca_slides}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("only", nargs="*", type=int)
    ap.add_argument("--out", default=str(ROOT / "media" / HANDLE))
    ap.add_argument("--no-story", action="store_true")
    a = ap.parse_args()
    out_root = Path(a.out)
    for p in POSTS:
        if a.only and p["n"] not in a.only:
            continue
        folder = out_root / f"post-{p['n']:02d}-{p['slug']}"
        folder.mkdir(parents=True, exist_ok=True)
        for i, h in enumerate(BUILD[p["format"]](p), 1):
            shoot(h, folder / f"slide-{i:02d}.png")
        (folder / "caption.txt").write_text(p["caption"].strip() + "\n", encoding="utf-8")
        if not a.no_story:
            shoot(story(p, folder / "slide-01.png"), out_root / f"story-{p['n']:02d}-{p['slug']}.png", (1080, 1920))
        print(folder.name)


if __name__ == "__main__":
    main()
