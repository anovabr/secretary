# -*- coding: utf-8 -*-
"""Stories para o dono postar À MÃO, com figurinha de link — no visual do story-01.

    python3 tools/slides/stories_link.py             # → stories-com-link/*.png + LEIA.txt
    python3 tools/slides/stories_link.py --out DIR   # prévia em outra pasta

A API do Instagram não põe figurinha de link, então estes stories NÃO vão para
media/anova.autismo/ (a fila publicaria sem link). Em vez do botão desenhado do
story-01, cada um deixa uma área tracejada vazia onde a figurinha entra.
"""

from __future__ import annotations

import argparse
import html
from datetime import date, timedelta
from pathlib import Path

from render import HERE, ROOT, HANDLE, asset, md, page, shoot

ADULT = ("https://autismo.anovasaude.org/test.html?instrument=rabesp-a"
         "&utm_source=instagram&utm_medium=story&utm_campaign={slug}")
CHILD = ("https://autismo.anovasaude.org/test-crianca.html"
         "?utm_source=instagram&utm_medium=story&utm_campaign={slug}")
STICKER = {"adulto": "Fazer o teste gratuito", "crianca": "Triagem para meu filho"}

# Ordem = ordem de postagem. [[palavra]] vai no destaque amarelo.
STORIES = [
    {"slug": "contato-visual", "who": "adulto", "article": "aprenda-mascaramento",
     "hook": "Você se obriga a olhar nos [[olhos]] de quem fala com você?",
     "text": "Forçar o contato visual, mesmo quando incomoda, é uma das formas de mascaramento. E manter isso cansa."},
    {"slug": "restaurante-cheio", "who": "adulto", "article": "aprenda-sensibilidade-sensorial",
     "hook": "Restaurante cheio te tira toda a [[energia]]?",
     "text": "Não é frescura. Barulho e movimento podem pesar muito mais do que parece de fora: é uma diferença real de processamento sensorial."},
    {"slug": "primeiras-palavras", "who": "crianca", "article": "aprenda-sinais-precoces",
     "hook": "Seu filho de 18 meses ainda não [[fala]]?",
     "text": "As primeiras palavras costumam vir entre 12 e 18 meses. Um atraso isolado raramente preocupa; vários atrasos juntos merecem atenção."},
    {"slug": "ironia", "who": "adulto", "article": "aprenda-comunicacao-social",
     "hook": "Você só entende a [[ironia]] depois que todo mundo já riu?",
     "text": "Captar tom de voz, ironia e o não dito pode exigir esforço consciente. Isso deixa as conversas mais cansativas."},
    {"slug": "plano-que-muda", "who": "adulto", "article": "aprenda-comportamentos-repetitivos",
     "hook": "Um plano que muda em cima da hora [[estraga]] o seu dia?",
     "text": "Rotina traz previsibilidade. Por isso uma mudança inesperada pode pesar muito mais do que o tamanho dela."},
    {"slug": "falas-do-desenho", "who": "crianca", "article": "aprenda-ecolalia",
     "hook": "Seu filho repete falas inteiras do [[desenho]]?",
     "text": "Isso se chama ecolalia. E repetir também comunica: pode ser um pedido, uma emoção ou um jeito de interagir."},
    {"slug": "assunto-que-prende", "who": "adulto", "article": "aprenda-interesses-e-hiperfoco",
     "hook": "É difícil [[largar]] um assunto que te prendeu?",
     "text": "Interesses intensos dão conhecimento de especialista, mas dificultam mudar de foco quando a situação pede."},
    {"slug": "comida-pela-cor", "who": "crianca", "article": "aprenda-seletividade-alimentar",
     "hook": "Seu filho recusa uma comida só pela [[cor]]?",
     "text": "Recusar comida pela cor, pela textura ou pelo cheiro costuma ter base sensorial real. Raramente é birra."},
]

START = date(2026, 11, 2)                       # segunda-feira
DAYS = [0, 1, 3, 5, 7, 8, 10, 12]               # seg, ter, qui, sáb × 2 semanas
WEEKDAY = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]

# Medidas tiradas do story-01-teste-adulto.png (avatar 66,72 · 106 px; texto a 67 px da borda).
CSS = """
body{background:#1a1a1a;color:#fff;font-family:'Work Sans'}
.who{position:absolute;left:66px;top:72px;display:flex;align-items:center}
.who img{width:106px;height:106px;border-radius:50%;object-fit:cover;display:block}
.who span{margin-left:28px;font-weight:500;font-size:44px;letter-spacing:.01em}
.txt{position:absolute;left:67px;right:100px;top:440px}
h1{font-weight:700;font-size:131px;line-height:1.07;letter-spacing:-.015em}
.hl{background:#fee11a;color:#1a1a1a;padding:0 .14em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
p{margin-top:64px;font-weight:400;font-size:54px;line-height:1.58;letter-spacing:.045em;color:#e6e3da}
.zone{position:absolute;left:190px;top:1500px;width:700px;height:200px;border:3px dashed rgba(255,255,255,.38);border-radius:28px}
.tap{position:absolute;left:0;right:0;top:1726px;text-align:center;font-weight:500;font-size:34px;letter-spacing:.04em;color:rgba(255,255,255,.62)}
.foot{position:absolute;left:0;right:0;top:1800px;text-align:center;font-weight:400;font-size:36px;letter-spacing:.04em;color:#b5b2a9}
"""

# Encolhe o título até o texto todo caber acima da área da figurinha.
FIT = """<script>
document.fonts.ready.then(function(){
  var h=document.querySelector('h1'), t=document.querySelector('.txt'), s=131;
  while(t.getBoundingClientRect().bottom>1420 && s>80){s-=4;h.style.fontSize=s+'px';}
});
</script>"""


def story_html(s: dict) -> str:
    body = (f'<div class="who"><img src="{asset("avatar-anova.png")}"><span>{HANDLE}</span></div>'
            f'<div class="txt"><h1>{md(s["hook"])}</h1><p>{md(s["text"])}</p></div>'
            '<div class="zone"></div><div class="tap">Toque no link</div>'
            '<div class="foot">Gratuito · Não substitui diagnóstico</div>' + FIT)
    return page(CSS, body, size=(1080, 1920))


def url(s: dict) -> str:
    return (ADULT if s["who"] == "adulto" else CHILD).format(slug=s["slug"])


def name(i: int, s: dict) -> str:
    return f"{i:02d}-{s['slug']}.png"


def leia() -> str:
    out = ["STORIES COM LINK — @anova.autismo",
           "",
           "Estes stories são para postar À MÃO. Eles não estão na fila automática",
           "(a API não coloca figurinha de link), então a secretária não os publica.",
           "",
           "Como postar:",
           "1. Abra o story no Instagram e escolha a imagem do dia nesta pasta.",
           "2. Toque no ícone de figurinhas, escolha \"Link\", cole a URL e digite o texto da figurinha.",
           "3. Posicione a figurinha sobre a área tracejada, acima de \"Toque no link\", e publique.",
           "",
           "Agenda (2 semanas, 4 por semana):",
           ""]
    for i, (s, d) in enumerate(zip(STORIES, DAYS), 1):
        day = START + timedelta(days=d)
        out += [f"{i}. {WEEKDAY[day.weekday()]}, {day:%d/%m/%Y} — {'adultos' if s['who'] == 'adulto' else 'pais'}",
                f"   Arquivo:            {name(i, s)}",
                f"   URL da figurinha:   {url(s)}",
                f"   Texto da figurinha: {STICKER[s['who']]}",
                ""]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "stories-com-link"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(STORIES, 1):
        shoot(story_html(s), out / name(i, s), (1080, 1920))
        print(name(i, s))
    (out / "LEIA.txt").write_text(leia(), encoding="utf-8")


if __name__ == "__main__":
    main()
