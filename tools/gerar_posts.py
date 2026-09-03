# -*- coding: utf-8 -*-
"""
Gera as imagens dos 20 carrosséis do Instagram/TikTok da ANOVA Autismo.
Saída: pasta "posts-imagens/post-XX-slug/slide-NN.png" (1080x1350, prontos para postar).

Uso:  python gerar_posts.py
Edite os textos na lista POSTS e rode de novo para regenerar.

Regras do template:
- Máximo de 5 slides por carrossel (capa + 3 conteúdos + CTA).
- Marca: símbolo "A" oficial (Luis - logos/logo-a.png.jpg) em todos os slides;
  logo horizontal oficial (Luis - logos/logo-autismo.png-removebg.png) no slide final.
- Afirmações factuais trazem a fonte científica em letra pequena ("ref").
"""

import os
from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------------------
# Identidade visual
# ----------------------------------------------------------------------------
W, H = 1080, 1350
BG = "#FFFFFF"  # branco puro: os logos oficiais (fundo branco) se fundem sem emenda
BLACK = "#1E1E24"
GOLD = "#C9A227"
GRAY = "#6B6B70"
RAINBOW = ["#E63329", "#F28C28", "#F7C700", "#3BA55D", "#2E6FD9", "#7A3E9D"]
URL = "autismo.anovasaude.org"

_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_A = os.path.join(_DIR, "Luis - logos", "logo-a.png.jpg")
LOGO_FULL = os.path.join(_DIR, "Luis - logos", "logo-autismo.png-removebg.png")

FONT_DIR = r"C:\Windows\Fonts"

def load_font(names, size):
    for n in names:
        p = os.path.join(FONT_DIR, n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def f_black(size):  # títulos
    return load_font(["seguibl.ttf", "segoeuib.ttf", "arialbd.ttf"], size)

def f_bold(size):
    return load_font(["segoeuib.ttf", "arialbd.ttf"], size)

def f_semi(size):
    return load_font(["seguisb.ttf", "segoeuib.ttf", "arial.ttf"], size)

def f_reg(size):
    return load_font(["segoeui.ttf", "arial.ttf"], size)

def f_ital(size):
    return load_font(["segoeuii.ttf", "segoeui.ttf", "arial.ttf"], size)

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def pale(color, t=0.75):
    r, g, b = hex2rgb(color)
    return (int(r + (255 - r) * t), int(g + (255 - g) * t), int(b + (255 - b) * t))

# Logos carregados uma única vez
_A_IMG = Image.open(LOGO_A).convert("RGB")
_FULL_IMG = Image.open(LOGO_FULL).convert("RGBA")

def paste_symbol(img, height, x, y):
    """Cola o símbolo 'A' oficial (JPEG fundo branco sobre slide branco)."""
    w = int(_A_IMG.width * height / _A_IMG.height)
    img.paste(_A_IMG.resize((w, height), Image.LANCZOS), (x, y))
    return w

# ----------------------------------------------------------------------------
# Utilidades de texto
# ----------------------------------------------------------------------------
def wrap(draw, text, font, maxw):
    lines = []
    for par in text.split("\n"):
        words, cur = par.split(), ""
        for w_ in words:
            trial = (cur + " " + w_).strip()
            if draw.textlength(trial, font=font) <= maxw:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w_
        lines.append(cur)
    return lines

def fit_text(draw, text, fontfn, start, minsize, maxw, maxh):
    size = start
    while size > minsize:
        font = fontfn(size)
        lines = wrap(draw, text, font, maxw)
        lh = int(size * 1.28)
        if len(lines) * lh <= maxh:
            return font, lines, lh
        size -= 4
    font = fontfn(minsize)
    lines = wrap(draw, text, font, maxw)
    return font, lines, int(minsize * 1.28)

# ----------------------------------------------------------------------------
# Elementos do template
# ----------------------------------------------------------------------------
def draw_progress(d, idx, total):
    r, gap = 10, 38
    x0 = W / 2 - (total - 1) * gap / 2
    y = 1258
    for i in range(total):
        c = RAINBOW[i % 6]
        rr = 14 if i == idx else r
        fill = hex2rgb(c) if i == idx else pale(c, 0.65)
        d.ellipse([x0 + i * gap - rr, y - rr, x0 + i * gap + rr, y + rr], fill=fill)

def draw_swipe(d):
    f = f_semi(34)
    t = "arraste  →"
    tw = d.textlength(t, font=f)
    d.text((W - 90 - tw, 1180), t, font=f, fill=GOLD)

def draw_ref(d, ref):
    """Fonte científica em letra pequena, canto inferior esquerdo."""
    font = f_ital(27)
    lines = wrap(d, ref, font, 640)[:2]
    y = 1160 - (len(lines) - 1) * 34
    for ln in lines:
        d.text((90, y), ln, font=font, fill=GRAY)
        y += 34

def new_slide():
    """Slide em branco com o símbolo 'A' no topo esquerdo."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    aw = paste_symbol(img, 110, 90, 52)
    f = f_semi(40)
    d.text((90 + aw + 26, 84), "ANOVA Autismo", font=f, fill=GRAY)
    return img, d

# ----------------------------------------------------------------------------
# Tipos de slide
# ----------------------------------------------------------------------------
def slide_cover(title, idx, total):
    img, d = new_slide()
    font, lines, lh = fit_text(d, title, f_black, 96, 60, 880, 640)
    y = (1350 - len(lines) * lh) / 2 - 40
    for ln in lines:
        d.text((100, y), ln, font=font, fill=BLACK)
        y += lh
    d.rounded_rectangle([100, y + 24, 320, y + 40], radius=8, fill=GOLD)
    draw_swipe(d)
    draw_progress(d, idx, total)
    return img

def slide_body(body, idx, total, head=None, ref=None):
    img, d = new_slide()
    top, bottom = 320, 1080
    if head:
        hf, hlines, hlh = fit_text(d, head, f_bold, 52, 38, 880, 260)
        block_h = len(hlines) * hlh + 40
    else:
        hlines, hlh, block_h, hf = [], 0, 0, None
    bf, blines, blh = fit_text(d, body, f_semi, 60, 42, 880, bottom - top - block_h)
    total_h = block_h + len(blines) * blh
    y = top + (bottom - top - total_h) / 2
    for ln in hlines:
        d.text((100, y), ln, font=hf, fill=GOLD)
        y += hlh
    if head:
        y += 40
    for ln in blines:
        d.text((100, y), ln, font=bf, fill=BLACK)
        y += blh
    if ref:
        draw_ref(d, ref)
    draw_swipe(d)
    draw_progress(d, idx, total)
    return img

def slide_cta(idx, total, note=None):
    """Slide final: logo horizontal oficial + hierarquia de conversão (versão aprovada)."""
    img = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(img)

    lw = 720
    lh = int(_FULL_IMG.height * lw / _FULL_IMG.width)
    logo = _FULL_IMG.resize((lw, lh), Image.LANCZOS)
    img.paste(logo, ((W - lw) // 2, 190), logo)
    y = 190 + lh + 70

    if note:
        nf, nlines, nlh = fit_text(d, note, f_semi, 44, 34, 880, 140)
        for ln in nlines:
            lwd = d.textlength(ln, font=nf)
            d.text(((W - lwd) / 2, y), ln, font=nf, fill=GRAY)
            y += nlh
        y += 30

    f1 = f_black(92)
    t1 = "Faça o teste gratuito"
    d.text(((W - d.textlength(t1, font=f1)) / 2, y), t1, font=f1, fill=BLACK)
    y += 165

    f2 = f_bold(56)
    t2 = "TOQUE NO LINK DA BIO"
    tw = d.textlength(t2, font=f2)
    bw, bh = tw + 140, 120
    bx, by = (W - bw) / 2, y
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=bh / 2, fill=GOLD)
    d.text(((W - tw) / 2, by + (bh - 56 * 1.28) / 2 + 7), t2, font=f2, fill="#FFFFFF")
    y = by + bh + 60

    f3 = f_semi(46)
    d.text(((W - d.textlength(URL, font=f3)) / 2, y), URL, font=f3, fill=BLACK)
    y += 80

    f4 = f_reg(38)
    t4 = "8 minutos  ·  sem cadastro  ·  resultado na hora"
    d.text(((W - d.textlength(t4, font=f4)) / 2, y), t4, font=f4, fill=GRAY)

    draw_progress(d, idx, total)
    return img

# ----------------------------------------------------------------------------
# Conteúdo dos 20 posts — SEMPRE 5 slides: capa + 3 conteúdos + CTA
# ----------------------------------------------------------------------------
# Formatos de slide:
#   {"cover": "..."}                           -> capa
#   {"body": "...", "ref": "fonte opcional"}   -> texto (aceita \n para listas)
#   {"head": "...", "body": "..."}             -> destaque dourado + texto
#   {"cta": None ou "nota"}                    -> slide final padrão (logo + CTA)
POSTS = [
    ("autismo-nao-tem-cara", [
        {"cover": "AUTISMO NÃO TEM CARA."},
        {"body": "Não existe “cara de autista”. O TEA é definido por critérios comportamentais — não por aparência.",
         "ref": "DSM-5-TR (APA, 2022)"},
        {"body": "Tem autista que fala muito. Tem autista que não fala. Tem autista com hiperfoco em astronomia. E tem autista que você jamais desconfiaria."},
        {"body": "O CDC estima 1 em cada 31 crianças no espectro — e a maioria dos adultos de hoje nunca foi avaliada. Se você sempre se sentiu “diferente”, investigar é autoconhecimento.",
         "ref": "CDC, ADDM Network (2025)"},
        {"cta": None},
    ]),
    ("5-sinais-em-adultos", [
        {"cover": "5 SINAIS DE AUTISMO EM ADULTOS QUE QUASE NINGUÉM PERCEBE"},
        {"head": "SINAIS 1–3", "body": "1. Exaustão após interações sociais — mesmo as que você gosta.\n2. Ensaiar conversas mentalmente antes (e depois) de tê-las.\n3. Incômodo intenso com sons, luzes, texturas ou etiquetas.",
         "ref": "Critérios A e B4 do DSM-5-TR"},
        {"head": "SINAIS 4–5", "body": "4. Interesses profundos e específicos que ocupam grande parte do pensamento.\n5. Sensação constante de estar “atuando” para parecer normal — a camuflagem (masking).",
         "ref": "Critério B3 do DSM-5-TR; Hull et al. (2017)"},
        {"body": "Identificou-se com 3 ou mais? Um rastreio psicométrico validado transforma essas percepções em escores comparáveis aos da população."},
        {"cta": None},
    ]),
    ("mulheres-no-espectro", [
        {"cover": "POR QUE TANTAS MULHERES AUTISTAS SÓ DESCOBREM DEPOIS DOS 30?"},
        {"body": "Os critérios diagnósticos foram construídos, historicamente, observando meninos. Conforme os métodos melhoram, a proporção homem:mulher cai de 4:1 para cerca de 3:1.",
         "ref": "Loomes, Hull & Mandy (2017), JAACAP"},
        {"body": "Meninas aprendem cedo a camuflar: imitam, ensaiam, forçam contato visual. E recebem rótulos errados — “tímida”, “ansiosa”, “dramática” — por décadas.",
         "ref": "CAT-Q: Hull et al. (2019)"},
        {"body": "O custo da camuflagem é documentado: ansiedade, depressão e exaustão. Muitas só se reconhecem quando um filho é diagnosticado.",
         "ref": "Cassidy et al. (2018); Cage & Troxell-Whitman (2019)"},
        {"cta": "Você se reconheceu?"},
    ]),
    ("mitos-e-verdades", [
        {"cover": "MITOS SOBRE AUTISMO QUE VOCÊ PROVAVELMENTE ACREDITA"},
        {"head": "MITO: “Autismo é doença.”", "body": "FATO: É uma condição do neurodesenvolvimento. Não se “cura” — se compreende e se apoia.",
         "ref": "DSM-5-TR (APA, 2022); CID-11 (OMS)"},
        {"head": "MITO: “Adulto que trabalha e namora não pode ser autista.”", "body": "FATO: Pode. O DSM-5-TR define níveis de suporte — e o nível 1 costuma ser invisível para quem está de fora."},
        {"head": "MITO: “Teste online não serve para nada.”", "body": "FATO: Rastreios validados, como o AQ, têm sensibilidade e especificidade documentadas em estudos revisados por pares.",
         "ref": "Baron-Cohen et al. (2001), J Autism Dev Disord"},
        {"cta": None},
    ]),
    ("rastreio-nao-e-diagnostico", [
        {"cover": "TESTE ONLINE DIAGNOSTICA AUTISMO? NÃO. E É IMPORTANTE QUE VOCÊ SAIBA DISSO."},
        {"body": "Diagnóstico de TEA é clínico: profissionais, entrevista, histórico de desenvolvimento. Mas antes dele existe uma etapa reconhecida pela literatura: o RASTREIO (screening)."},
        {"body": "O rastreio responde: “faz sentido investigar mais a fundo?” — com instrumentos psicométricos de sensibilidade e especificidade conhecidas.",
         "ref": "Ex.: AQ — Baron-Cohen et al. (2001)"},
        {"body": "É como um exame preventivo: não conclui, mas orienta o próximo passo com evidência. Na ANOVA, é gratuito, leva 8 minutos e o resultado sai na hora."},
        {"cta": "Comece sua investigação do jeito certo."},
    ]),
    ("masking", [
        {"cover": "VOCÊ SE FANTASIA DE “NORMAL” TODOS OS DIAS? A CIÊNCIA CHAMA ISSO DE MASKING."},
        {"body": "Masking (camuflagem social) é suprimir traços autistas para se encaixar: forçar contato visual, copiar gestos, ensaiar falas. É um construto medido pela ciência.",
         "ref": "CAT-Q: Hull et al. (2019)"},
        {"body": "Parece adaptação, mas é trabalho cognitivo em tempo integral. O custo é documentado: ansiedade, depressão e burnout autista.",
         "ref": "Cassidy et al. (2018); Raymaker et al. (2020)"},
        {"body": "Reconhecer o masking costuma ser o primeiro fio que puxa a descoberta do espectro em adultos."},
        {"cta": "Puxe esse fio."},
    ]),
    ("sinais-em-criancas", [
        {"cover": "SINAIS PRECOCES DE AUTISMO: O QUE OBSERVAR NO SEU FILHO"},
        {"body": "• Pouco contato visual; não apontar para compartilhar interesse.\n• Atraso na fala — ou fala muito formal para a idade.\n• Movimentos repetitivos, rotinas rígidas.\n• Reações intensas a sons, texturas e mudanças.",
         "ref": "Critérios A e B do DSM-5-TR; Zwaigenbaum et al. (2015)"},
        {"body": "Sinais não são sentença. A recomendação internacional é rastrear formalmente aos 18 e 24 meses.",
         "ref": "AAP: M-CHAT-R/F aos 18 e 24 meses"},
        {"body": "Quanto mais cedo a identificação, maiores os ganhos com intervenção precoce. Isso é consenso científico.",
         "ref": "Zwaigenbaum et al. (2015), Pediatrics"},
        {"cta": "Em breve: rastreio infantil na ANOVA. Enquanto isso, conheça a plataforma."},
    ]),
    ("diagnostico-tardio", [
        {"cover": "“JÁ TENHO 40 ANOS. AINDA VALE A PENA SABER SE SOU AUTISTA?”"},
        {"body": "Vale. A pesquisa com adultos diagnosticados tardiamente relata o mesmo tema: alívio e autocompreensão. “Finalmente minha vida inteira fez sentido.”",
         "ref": "Stagg & Belcher (2019); Leedham et al. (2020)"},
        {"body": "O diagnóstico (ou a suspeita bem fundamentada) permite: entender seus limites, negociar adaptações no trabalho, cuidar da saúde mental com a abordagem certa."},
        {"body": "E o mais importante: trocar décadas de “o que há de errado comigo?” por “é assim que meu cérebro funciona”."},
        {"cta": "Não é tarde. Comece hoje."},
    ]),
    ("como-funciona-anova", [
        {"cover": "COMO FUNCIONA O TESTE DE RASTREIO DA ANOVA?"},
        {"head": "PASSOS 1 E 2", "body": "Você responde 12 perguntas sobre seu jeito de perceber e interagir com o mundo. Cerca de 8 minutos, sem cadastro, gratuito."},
        {"head": "PASSOS 3 E 4", "body": "O resultado sai na hora, com base em instrumentos validados. Quer ir além? O relatório detalhado (R$29,90) interpreta seus escores em comparação com dados populacionais."},
        {"body": "Transparência: rastreio orienta a investigação — não substitui avaliação clínica. E seus dados são protegidos."},
        {"cta": None},
    ]),
    ("neurodiversidade", [
        {"cover": "E SE NÃO HOUVER NADA DE “ERRADO” COM VOCÊ?"},
        {"body": "Neurodiversidade é a ideia de que cérebros humanos variam — como alturas, vozes e impressões digitais. Autismo, TDAH e dislexia são variações do neurodesenvolvimento.",
         "ref": "Termo cunhado por Judy Singer (1998)"},
        {"body": "Isso não significa romantizar as dificuldades. Suporte é necessário — e é um direito garantido em lei.",
         "ref": "No Brasil: Lei Berenice Piana (12.764/2012)"},
        {"body": "Significa trocar “como conserto isso?” por “de que suporte eu preciso para funcionar bem?”"},
        {"cta": "Conhecer seu cérebro é o primeiro passo."},
    ]),
    ("frases-que-autistas-ouvem", [
        {"cover": "FRASES QUE TODO AUTISTA JÁ CANSOU DE OUVIR"},
        {"head": "“Mas você não parece autista.”", "body": "Autismo não é aparência. É um diagnóstico definido por critérios comportamentais.",
         "ref": "DSM-5-TR (APA, 2022)"},
        {"head": "“Todo mundo é um pouco autista.”", "body": "Não. Traços existem na população geral, mas o diagnóstico exige prejuízo funcional significativo — é outra coisa."},
        {"head": "“Isso é frescura.”", "body": "Processamento sensorial atípico é critério diagnóstico. É neurologia, não drama.",
         "ref": "Critério B4 do DSM-5-TR"},
        {"cta": "Cansou de ouvir e quer respostas de verdade?"},
    ]),
    ("hiperfoco", [
        {"cover": "HIPERFOCO: O LADO DO AUTISMO QUE NINGUÉM EXPLICA DIREITO"},
        {"body": "Hiperfoco é mergulhar tão fundo em um interesse que o mundo ao redor desaparece. É de onde vêm coleções enciclopédicas e carreiras brilhantes."},
        {"body": "Mas também é esquecer de comer, de dormir, de responder mensagens — e ser cobrado por isso."},
        {"body": "Não é “superpoder” nem “defeito”. Interesses restritos e intensos são critério diagnóstico — e um dos marcadores avaliados em rastreios validados.",
         "ref": "Critério B3 do DSM-5-TR"},
        {"cta": None},
    ]),
    ("sobrecarga-sensorial", [
        {"cover": "POR QUE O SUPERMERCADO TE DEIXA EXAUSTO(A)?"},
        {"body": "Luz fluorescente + música + conversas cruzadas + etiqueta da blusa... Para muitos cérebros autistas, os estímulos não são “filtrados” — chegam todos juntos, no volume máximo.",
         "ref": "Hiperreatividade sensorial: critério B4 do DSM-5-TR"},
        {"body": "O resultado pode ser: irritabilidade, fadiga extrema, shutdown (desligamento) ou meltdown (crise). Não é falta de educação. É neurologia."},
        {"body": "Fones abafadores, listas prontas, horários vazios: pequenas adaptações baseadas em evidência mudam a rotina."},
        {"cta": "Entenda como seu cérebro processa o mundo."},
    ]),
    ("autismo-no-trabalho", [
        {"cover": "AUTISTAS NO TRABALHO: O TALENTO QUE AS EMPRESAS NÃO APRENDERAM A VER"},
        {"body": "Atenção a detalhes. Honestidade direta. Profundidade técnica. E ainda assim, estimativas internacionais apontam desemprego ou subemprego de até 80% entre autistas adultos.",
         "ref": "ONU (2015); Office for National Statistics, UK (2021)"},
        {"body": "O problema raramente é a competência. São entrevistas que avaliam carisma, escritórios abertos e regras sociais não ditas."},
        {"body": "Adaptações simples — comunicação clara, previsibilidade, ambiente sensorial adequado — destravam carreiras. Autoconhecimento é o primeiro passo para negociá-las."},
        {"cta": "Comece por você."},
    ]),
    ("rastreio-positivo-e-agora", [
        {"cover": "SEU TESTE DEU POSITIVO PARA TRAÇOS AUTISTAS. E AGORA?"},
        {"body": "Primeiro: respira. Um rastreio positivo não é diagnóstico — é um indicador estatístico de que vale investigar."},
        {"head": "PASSOS 1 E 2", "body": "Guarde seu relatório: ele organiza escores para apresentar a um profissional. E procure psicólogo ou psiquiatra com experiência em TEA adulto."},
        {"head": "PASSOS 3 E 4", "body": "Registre situações de sobrecarga e camuflagem — histórico é parte central da avaliação. E conecte-se: apoio entre pares é associado a melhor bem-estar.",
         "ref": "Crompton et al. (2020), Autism"},
        {"cta": "Ainda não fez o rastreio?"},
    ]),
    ("burnout-autista-mulheres", [
        {"cover": "ELA NÃO É “FORTE DEMAIS PARA QUEBRAR”. BURNOUT AUTISTA EM MULHERES."},
        {"body": "O burnout autista foi descrito na literatura: exaustão crônica, perda de habilidades e redução da tolerância a estímulos — após anos de demandas acima da capacidade.",
         "ref": "Raymaker et al. (2020), Autism in Adulthood"},
        {"body": "Décadas de camuflagem cobram juros — e a camuflagem é mais frequente e intensa entre mulheres.",
         "ref": "Hull et al. (2020); Lai et al. (2017)"},
        {"body": "Muitas são tratadas para depressão e ansiedade durante anos, sem ninguém investigar o que há por baixo. Quando o tratamento ignora o espectro, ele enxuga gelo."},
        {"cta": "A resposta certa começa com a pergunta certa."},
    ]),
    ("psicometria-confiavel", [
        {"cover": "O QUE FAZ UM TESTE PSICOLÓGICO SER CONFIÁVEL?"},
        {"body": "Qualquer um pode publicar um quiz “descubra se você é autista”. Psicometria é outra coisa — uma disciplina científica com padrões internacionais.",
         "ref": "Standards for Educational and Psychological Testing (AERA/APA/NCME)"},
        {"body": "VALIDADE: o teste mede o que promete medir.\nFIDEDIGNIDADE: os resultados são consistentes.\nNORMATIZAÇÃO: seus escores são comparados com dados reais da população."},
        {"body": "A ANOVA nasceu da psicometria: rastreios validados — e clareza sobre o que eles podem e não podem afirmar."},
        {"cta": "Teste sério, resultado na hora."},
    ]),
    ("criancas-viram-adultos", [
        {"cover": "CRIANÇAS AUTISTAS VIRAM ADULTOS AUTISTAS."},
        {"body": "A maior parte do conteúdo, dos serviços e das pesquisas mira a infância. Mas o espectro não expira aos 18.",
         "ref": "Lai & Baron-Cohen (2015), Lancet Psychiatry"},
        {"body": "A literatura chama os adultos que cresceram sem acesso a diagnóstico de “geração perdida”. Hoje, eles se descobrem sozinhos, pesquisando à noite."},
        {"body": "Se você é esse adulto: você não está atrasado. O acesso é que chegou tarde."},
        {"cta": "Comece agora, em 8 minutos."},
    ]),
    ("checklist-rastreio", [
        {"cover": "VOCÊ DEVERIA FAZER UM RASTREIO DE AUTISMO? FAÇA O TESTE DO TESTE."},
        {"body": "[  ] Sinto que “atuo” em situações sociais.\n[  ] Rotinas quebradas me desorganizam demais.\n[  ] Tenho interesses intensos que acham “demais”."},
        {"body": "[  ] Sons, luzes ou texturas me incomodam num nível difícil de explicar.\n[  ] Sempre me senti “de fora”, mesmo entre amigos."},
        {"body": "Marcou 3 ou mais? Um rastreio psicométrico validado transforma essas percepções em escores comparáveis aos da população.",
         "ref": "Itens ilustrativos, inspirados em domínios do AQ — Baron-Cohen et al. (2001)"},
        {"cta": None},
    ]),
    ("por-que-criamos-a-anova", [
        {"cover": "POR QUE CRIAMOS A ANOVA AUTISMO?"},
        {"body": "Porque a fila para avaliação de TEA no Brasil é longa, cara e concentrada nos grandes centros — e quem busca resposta só encontra quiz de entretenimento ou consulta a R$800."},
        {"body": "Nossa proposta: rastreio psicométrico com validade e fidedignidade documentadas. 12 perguntas, 8 minutos, sem cadastro, relatório detalhado opcional, dados protegidos."},
        {"body": "Rastreio não substitui diagnóstico — e quem te disser o contrário não está do lado da ciência."},
        {"cta": "Conheça a plataforma e siga a gente."},
    ]),
]

# ----------------------------------------------------------------------------
# Geração
# ----------------------------------------------------------------------------
def main():
    base = os.path.join(_DIR, "posts-imagens")
    os.makedirs(base, exist_ok=True)
    total_imgs = 0
    for n, (slug, slides) in enumerate(POSTS, start=1):
        assert len(slides) == 5, f"post {slug} tem {len(slides)} slides (máximo/padrão: 5)"
        folder = os.path.join(base, f"post-{n:02d}-{slug}")
        os.makedirs(folder, exist_ok=True)
        total = len(slides)
        for i, s in enumerate(slides):
            if "cover" in s:
                img = slide_cover(s["cover"], i, total)
            elif "cta" in s:
                img = slide_cta(i, total, s["cta"])
            else:
                img = slide_body(s["body"], i, total, head=s.get("head"), ref=s.get("ref"))
            img.save(os.path.join(folder, f"slide-{i + 1:02d}.png"))
            total_imgs += 1
        print(f"post-{n:02d}-{slug}: {total} slides")
    print(f"\nOK: {total_imgs} imagens geradas em {base}")

if __name__ == "__main__":
    main()
