# -*- coding: utf-8 -*-
"""Textos dos carrosséis 55–64 (anova.autismo), renderizados por render.py.

Marcação dentro dos textos:  **negrito**   [[destaque amarelo/colorido]]
Formatos (docs/formatos.md):  dsm (série DSM-5 na vida real, como o post 39),
foto (A, "Precisamos falar"), conheca (B, perguntas).
"""

CLOSE = (
    "Faça o rastreio gratuito no link da bio — 8 minutos, sem cadastro, resultado na hora.\n"
    "autismo.anovasaude.org\n\n"
    "Rastreio não é diagnóstico: o resultado serve para orientar a busca por uma avaliação profissional."
)

POSTS = [
    # ------------------------------------------------------------------ 55
    {
        "n": 55, "slug": "dsm5-comunicacao-nao-verbal", "format": "dsm",
        "ref": "DSM-5-TR, critério A2 (APA, 2022)",
        "cover": {
            "kicker": "Critério A · Aspecto 2",
            "title": "Déficits na comunicação não verbal",
            "lead": "Olhar, gestos, expressão.",
            "punch": "O que o corpo diz — ou não diz — numa conversa.",
        },
        "examples": [
            {"manual": "Comunicação verbal e não verbal pouco integradas.",
             "real": ["Você conta uma boa notícia com a mesma cara de quando está entediado — e ninguém acredita.",
                      "Faz uma piada sem sorrir e precisa avisar: “é brincadeira”."],
             "note": "Não é frieza. A emoção existe; o rosto é que não acompanha no automático."},
            {"manual": "Diferenças no contato visual e na linguagem corporal.",
             "real": ["Olhar nos olhos exige tanto esforço que você para de ouvir o que a pessoa diz.",
                      "Na conversa, você olha para a boca, para a mão ou para um ponto atrás da pessoa."],
             "note": "Não é desrespeito. Muitas vezes é o jeito de conseguir prestar atenção."},
            {"manual": "Dificuldade em entender e usar gestos e expressões faciais.",
             "real": ["Alguém revira os olhos e você não sabe se foi para você.",
                      "Te dizem que você parece bravo quando está só concentrado."],
             "note": "O recado não verbal chega com ruído — nos dois sentidos."},
        ],
        "cta": {"comment": "Qual você mais vive: 1, 2 ou 3?", "remember": "Um exemplo sozinho não é diagnóstico."},
        "caption": """Déficits na comunicação não verbal: o nome é técnico, a cena é de toda semana.

É o segundo aspecto do critério A do DSM-5-TR. Na vida real, pode ser contar uma boa notícia com cara de tédio. Olhar para a boca da pessoa em vez dos olhos — porque é o jeito de conseguir ouvir. Não saber se aquele revirar de olhos foi para você. Ouvir que parece bravo quando está só concentrado.

Não é frieza nem falta de educação. O que sente existe; o que não vem no automático é o canal do rosto, do olhar e dos gestos.

Um exemplo sozinho não é diagnóstico. Qual você mais vive: 1, 2 ou 3?

DSM-5-TR, critério A2 (APA, 2022).

{CLOSE}

#DSM5 #autismoadulto #comunicacaonaoverbal #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 56
    {
        "n": 56, "slug": "meltdown-e-shutdown", "format": "foto", "motif": "wave",
        "ref": "Phung et al. (2021), Frontiers in Psychology",
        "cover": {
            "pre": "Precisamos falar sobre",
            "hl": "meltdown e shutdown",
            "sub": "**Não é birra.** E entender a diferença **muda tudo**.",
        },
        "body": [
            {"kicker": "Meltdown",
             "text": "É quando o sistema [[passa do limite]]: barulho, cobrança, mudança e cansaço ao mesmo tempo.",
             "more": "Pode vir com choro, grito ou movimento intenso. Não é escolha."},
            {"kicker": "Shutdown",
             "text": "Por fora, o oposto. Por dentro, o mesmo: a pessoa [[se desliga]].",
             "more": "Para de falar, de responder, de conseguir decidir. Parece calma. Não está."},
            {"kicker": "O que ajuda",
             "text": "Jovens autistas contam que piora quando são [[mal interpretados]] — e melhora com compreensão de quem está perto.",
             "more": "Paciência e parceria de adultos de confiança fazem diferença."},
        ],
        "cta": {"lead": "Se você se reconheceu,", "hl": "vale fazer um rastreio."},
        "caption": """Não é birra. Meltdown e shutdown são outra coisa — e confundir os dois com “manha” machuca.

Meltdown é quando o sistema passa do limite: barulho, cobrança, mudança e cansaço ao mesmo tempo. Pode vir com choro, grito ou movimento intenso.

Shutdown é o contrário por fora e o mesmo por dentro: a pessoa se desliga. Para de falar, de responder, de decidir. Parece calma — não está.

Num estudo em que jovens autistas descreveram essas experiências, eles contaram que tudo piora quando são mal interpretados pelos adultos, e melhora com compreensão e parceria de quem confiam.

Phung et al. (2021), Frontiers in Psychology.

{CLOSE}

#meltdown #shutdown #autismoadulto #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 57
    {
        "n": 57, "slug": "autismo-e-genetico", "format": "conheca",
        "ref": "Bai et al. (2019), JAMA Psychiatry · Ozonoff et al. (2024), Pediatrics",
        "cover": {
            "lines": [("Autismo é", "plain"), ("genético?", "pink")],
            "sub": "A resposta curta: em grande parte, sim.",
            "people": ["person_raising_hand-medium", "woman_technologist-medium", "man_tipping_hand-medium-dark", "woman_tipping_hand-medium-light"],
        },
        "body": [
            {"kicker": "Em grande parte, sim", "emoji": "dna",
             "head": "Cerca de [[80%]]",
             "text": "Um estudo com 2 milhões de pessoas em 5 países estimou que cerca de 80% da variação no risco de autismo vem de fatores herdados.",
             "ref": "Bai et al. (2019), JAMA Psychiatry"},
            {"kicker": "Não é culpa da criação", "emoji": "red_heart",
             "head": "Não é [[o jeito de criar]]",
             "text": "O mesmo estudo não encontrou contribuição relevante de efeitos maternos. Autismo não vem de falta de carinho nem de “mãe fria”.",
             "ref": "Bai et al. (2019), JAMA Psychiatry"},
            {"kicker": "Na família", "emoji": "people_hugging",
             "head": "[[1 em cada 5]] irmãos",
             "text": "Entre irmãos mais novos de crianças autistas, cerca de 20% também receberam o diagnóstico até os 3 anos.",
             "ref": "Ozonoff et al. (2024), Pediatrics"},
        ],
        "cta": {"lead": "Tem autismo na família?", "head": "Faça o rastreio gratuito"},
        "caption": """Autismo é genético? Em grande parte, sim.

Um estudo com mais de 2 milhões de pessoas em cinco países estimou que cerca de 80% da variação no risco de autismo vem de fatores herdados. O mesmo estudo não encontrou contribuição relevante de efeitos maternos: autismo não é resultado de criação, falta de carinho ou “mãe fria”.

Na família, isso aparece: entre irmãos mais novos de crianças autistas, cerca de 1 em cada 5 também recebeu o diagnóstico até os 3 anos.

Bai et al. (2019), JAMA Psychiatry; Ozonoff et al. (2024), Pediatrics.

{CLOSE}

#genetica #autismo #familia #autismoadulto #TEA""",
    },
    # ------------------------------------------------------------------ 58
    {
        "n": 58, "slug": "dsm5-relacionamentos", "format": "dsm",
        "ref": "DSM-5-TR, critério A3 (APA, 2022)",
        "cover": {
            "kicker": "Critério A · Aspecto 3",
            "title": "Déficits para desenvolver e manter relacionamentos",
            "lead": "Querer perto e não saber como.",
            "punch": "Amizade, trabalho, festa: as regras que ninguém escreveu.",
        },
        "examples": [
            {"manual": "Dificuldade em ajustar o comportamento a diferentes contextos sociais.",
             "real": ["Você fala com o chefe do mesmo jeito que fala com um amigo — e só percebe pela reação.",
                      "Numa festa, não sabe a hora de entrar numa roda nem a hora de sair dela."],
             "note": "Não é falta de noção. As regras sociais mudam de lugar para lugar e não vêm escritas."},
            {"manual": "Dificuldade em fazer amigos.",
             "real": ["Você quer amigos, mas não sabe como transformar um colega em amigo.",
                      "Depois de um encontro bom, não sabe se é a sua vez de chamar de novo."],
             "note": "Solidão nem sempre é escolha. Às vezes é o caminho que não ficou claro."},
            {"manual": "Pouco interesse aparente pela convivência com os pares.",
             "real": ["Você prefere uma conversa longa com uma pessoa a dez conversas rápidas num grupo.",
                      "Recusa convites não por desinteresse, mas porque socializar te deixa exausto por dias."],
             "note": "Querer companhia e se cansar dela podem acontecer ao mesmo tempo."},
        ],
        "cta": {"comment": "Qual você mais vive: 1, 2 ou 3?", "remember": "Um exemplo sozinho não é diagnóstico."},
        "caption": """Querer perto e não saber como. É o terceiro aspecto do critério A do DSM-5-TR.

Na vida real, pode ser falar com o chefe do mesmo jeito que com um amigo e só perceber pela reação. Querer amigos e não saber transformar um colega em amigo. Não saber se é a sua vez de chamar de novo. Recusar um convite não por desinteresse, mas porque socializar cansa por dias.

Não é falta de noção nem de afeto. As regras sociais mudam de lugar para lugar — e quase nunca vêm escritas.

Um exemplo sozinho não é diagnóstico. Qual você mais vive: 1, 2 ou 3?

DSM-5-TR, critério A3 (APA, 2022).

{CLOSE}

#DSM5 #autismoadulto #amizade #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 59
    {
        "n": 59, "slug": "inercia-autista", "format": "foto", "motif": "loading",
        "ref": "Buckle et al. (2021), Frontiers in Psychology",
        "cover": {
            "pre": "Precisamos falar sobre",
            "hl": "inércia autista",
            "sub": "Quando você **quer começar** — e o corpo **não vai**.",
        },
        "body": [
            {"kicker": "O que é",
             "text": "Dificuldade de [[começar, parar ou trocar]] de atividade — mesmo querendo muito.",
             "more": "Num estudo com 32 adultos autistas, eles descreveram isso como algo fora do controle consciente."},
            {"kicker": "Na prática",
             "text": "Ficar uma hora olhando para a louça. Saber que precisa responder a mensagem e [[não conseguir]].",
             "more": "E o outro lado: não conseguir parar o que está fazendo para ir dormir."},
            {"kicker": "O que ajuda",
             "text": "Os participantes contaram que um [[empurrão de fora]] ajuda: um lembrete, alguém que começa junto.",
             "more": "E que o estresse e a saúde mental abalada pioram a inércia."},
        ],
        "cta": {"lead": "Se você se reconheceu,", "hl": "vale fazer um rastreio."},
        "caption": """Não é preguiça. Tem nome: inércia autista.

É a dificuldade de começar, parar ou trocar de atividade — mesmo querendo muito. Ficar uma hora olhando para a louça. Saber que precisa responder a mensagem e não conseguir. Ou o contrário: não conseguir parar o que está fazendo para ir dormir.

No primeiro estudo dedicado ao tema, 32 adultos autistas descreveram essa experiência como algo fora do controle consciente. Contaram que um empurrão de fora ajuda — um lembrete, alguém que começa junto — e que o estresse piora.

Buckle et al. (2021), Frontiers in Psychology.

{CLOSE}

#inerciaautista #funcoesexecutivas #autismoadulto #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 60
    {
        "n": 60, "slug": "quantas-pessoas-sao-autistas", "format": "conheca",
        "ref": "IBGE, Censo 2022 (2025) · CDC, ADDM Network (2025)",
        "cover": {
            "lines": [("Quantas pessoas", "plain"), ("são autistas?", "blue")],
            "sub": "Os números mais recentes, do Brasil e dos EUA.",
            "people": ["woman_raising_hand-medium-dark", "man_raising_hand-medium-light", "person_raising_hand-medium", "teacher-medium-dark"],
        },
        "body": [
            {"kicker": "No Brasil", "emoji": "bar_chart",
             "head": "[[2,4 milhões]]",
             "text": "O Censo 2022 perguntou, pela primeira vez, quem já tinha diagnóstico de autismo: 1,2% da população.",
             "ref": "IBGE, Censo Demográfico 2022 (2025)"},
            {"kicker": "Nos EUA", "emoji": "magnifying_glass_tilted_left",
             "head": "[[1 em cada 31]] crianças",
             "text": "É a estimativa aos 8 anos da rede de vigilância do CDC, com dados de 2022. Na contagem anterior, era 1 em 36.",
             "ref": "CDC, ADDM Network (2025)"},
            {"kicker": "Por que sobe", "emoji": "light_bulb",
             "head": "Mais [[identificação]]",
             "text": "O próprio CDC atribui parte da variação a diferenças em como cada lugar identifica o autismo. E o Censo conta só quem já tem diagnóstico.",
             "ref": "CDC, ADDM Network (2025) · IBGE (2025)"},
        ],
        "cta": {"lead": "Ainda não foi avaliado?", "head": "Faça o rastreio gratuito"},
        "caption": """Quantas pessoas são autistas? Os números mais recentes.

No Brasil, o Censo 2022 perguntou pela primeira vez quem já tinha diagnóstico de autismo: 2,4 milhões de pessoas, 1,2% da população.

Nos EUA, a rede de vigilância do CDC estimou 1 em cada 31 crianças de 8 anos, com dados de 2022 — na contagem anterior, era 1 em 36. O próprio CDC aponta que parte da variação reflete diferenças em como cada lugar identifica o autismo.

E o Censo só conta quem já tem diagnóstico. Quem nunca foi avaliado não aparece nessa conta.

IBGE, Censo Demográfico 2022 (2025); CDC, ADDM Network (2025).

{CLOSE}

#censo2022 #prevalencia #autismo #autismoadulto #TEA""",
    },
    # ------------------------------------------------------------------ 61
    {
        "n": 61, "slug": "dsm5-movimentos-repetitivos", "format": "dsm",
        "ref": "DSM-5-TR, critério B1 (APA, 2022)",
        "cover": {
            "kicker": "Critério B · Aspecto 1",
            "title": "Movimentos, uso de objetos ou fala repetitivos",
            "lead": "Balançar, alinhar, repetir.",
            "punch": "O corpo também tem jeitos próprios de se organizar.",
        },
        "examples": [
            {"manual": "Movimentos motores estereotipados ou repetitivos.",
             "real": ["Você balança a perna ou o corpo para conseguir se concentrar.",
                      "Mexe as mãos ou os dedos quando está muito feliz — ou muito nervoso."],
             "note": "Muitas vezes é autorregulação. Interromper nem sempre ajuda."},
            {"manual": "Uso repetitivo de objetos.",
             "real": ["Você organiza objetos em fileiras ou por cor, e isso acalma.",
                      "Gira a caneta, o anel ou a tampinha durante a reunião inteira."],
             "note": "Não é mania boba. Pode ser o que mantém a cabeça no lugar."},
            {"manual": "Fala repetitiva ou frases idiossincráticas, como a ecolalia.",
             "real": ["Você repete uma fala de filme porque ela diz exatamente o que você sente.",
                      "Repete uma palavra baixinho porque o som é bom."],
             "note": "Repetir também pode ser comunicar — e se acalmar."},
        ],
        "cta": {"comment": "Qual você mais vive: 1, 2 ou 3?", "remember": "Um exemplo sozinho não é diagnóstico."},
        "caption": """Balançar, alinhar, repetir. É o primeiro aspecto do critério B do DSM-5-TR.

Na vida real, pode ser balançar a perna para conseguir se concentrar. Mexer as mãos quando está muito feliz. Organizar objetos por cor porque isso acalma. Girar a caneta a reunião inteira. Repetir uma fala de filme porque ela diz exatamente o que você sente.

Não é mania boba. Muitas vezes é o jeito que o corpo encontrou de se organizar.

Um exemplo sozinho não é diagnóstico. Qual você mais vive: 1, 2 ou 3?

DSM-5-TR, critério B1 (APA, 2022).

{CLOSE}

#DSM5 #stimming #autismoadulto #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 62
    {
        "n": 62, "slug": "interocepcao", "format": "foto", "motif": "pulse",
        "ref": "Garfinkel et al. (2016), Biological Psychology",
        "cover": {
            "pre": "Precisamos falar sobre",
            "hl": "interocepção",
            "sub": "Perceber **fome, sede, dor** — e o que **você sente**.",
        },
        "body": [
            {"kicker": "O que é",
             "text": "É o sentido que lê [[o que acontece dentro do corpo]]: coração, fome, bexiga, respiração.",
             "more": "É também por ele que a gente reconhece as próprias emoções."},
            {"kicker": "No autismo",
             "text": "Num estudo, adultos autistas perceberam os próprios batimentos [[com menos precisão]] —",
             "more": "embora relatassem sentir muito o corpo. Essa diferença se associou a mais ansiedade."},
            {"kicker": "Na vida real",
             "text": "Perceber a fome só quando já está tonto. Notar a ansiedade [[só pela dor de cabeça]].",
             "more": "Nem todo autista vive isso, e nem todo mundo que vive é autista."},
        ],
        "cta": {"lead": "Se você se reconheceu,", "hl": "vale fazer um rastreio."},
        "caption": """Perceber a fome só quando já está tonto. Notar que estava ansioso só pela dor de cabeça no fim do dia.

Isso tem nome: interocepção. É o sentido que lê o que acontece dentro do corpo — coração, fome, bexiga, respiração. É também por ele que a gente reconhece as próprias emoções.

Num estudo, adultos autistas perceberam os próprios batimentos com menos precisão, embora relatassem sentir muito o corpo. Quanto maior essa diferença, mais sintomas de ansiedade.

Nem todo autista vive isso, e nem todo mundo que vive é autista.

Garfinkel et al. (2016), Biological Psychology.

{CLOSE}

#interocepcao #ansiedade #autismoadulto #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 63
    {
        "n": 63, "slug": "o-que-e-ecolalia", "format": "conheca",
        "ref": "Prizant & Duchan (1981) · Sterponi & Shankey (2014)",
        "cover": {
            "lines": [("O que é", "plain"), ("ecolalia?", "pink")],
            "sub": "Repetir falas também pode ser se comunicar.",
            "people": ["woman_gesturing_ok-medium", "health_worker-medium-light", "person_tipping_hand-medium", "teacher-medium-dark"],
        },
        "body": [
            {"kicker": "O que é", "emoji": "speaking_head",
             "head": "Repetir [[o que ouviu]]",
             "text": "Palavras ou frases de outras pessoas, de desenhos, de filmes — logo depois de ouvir ou dias mais tarde.",
             "ref": "DSM-5-TR, critério B1 (APA, 2022)"},
            {"kicker": "Não é fala vazia", "emoji": "repeat_button",
             "head": "Tem [[função]]",
             "text": "Num estudo com mais de mil falas, a ecolalia serviu para responder, pedir, concordar e manter a conversa.",
             "ref": "Prizant & Duchan (1981)"},
            {"kicker": "Como responder", "emoji": "thinking_face",
             "head": "[[O que essa frase]] quer dizer agora?",
             "text": "A mesma frase pode marcar posições diferentes conforme o tom. Entender ajuda mais do que corrigir.",
             "ref": "Sterponi & Shankey (2014), J Child Lang"},
        ],
        "cta": {"lead": "Ficou com dúvida?", "head": "Faça o rastreio gratuito"},
        "caption": """O que é ecolalia? É repetir palavras ou frases ouvidas — de outras pessoas, de desenhos, de filmes — logo depois ou dias mais tarde.

Por muito tempo, isso foi tratado como fala sem sentido. Mas, num estudo com mais de mil falas, a ecolalia serviu para responder, pedir, concordar e manter a conversa. Pesquisas mais recentes mostram que a mesma frase pode marcar posições diferentes conforme o tom.

Por isso, entender ajuda mais do que corrigir: o que essa frase quer dizer agora?

DSM-5-TR, critério B1 (APA, 2022); Prizant & Duchan (1981); Sterponi & Shankey (2014).

{CLOSE}

#ecolalia #comunicacao #autismo #autismoinfantil #TEA""",
    },
    # ------------------------------------------------------------------ 64
    {
        "n": 64, "slug": "dsm5-rotinas-e-mudancas", "format": "dsm",
        "ref": "DSM-5-TR, critério B2 (APA, 2022)",
        "cover": {
            "kicker": "Critério B · Aspecto 2",
            "title": "Insistência nas mesmas coisas e nas rotinas",
            "lead": "Mesmo caminho, mesmo café.",
            "punch": "Quando a previsibilidade é o que deixa o dia possível.",
        },
        "examples": [
            {"manual": "Sofrimento intenso com pequenas mudanças.",
             "real": ["O restaurante mudou o cardápio e o seu dia saiu do eixo.",
                      "Uma reunião remarcada em cima da hora estraga a tarde inteira."],
             "note": "Não é frescura. Previsibilidade é o que sobra de energia para o resto."},
            {"manual": "Dificuldade com transições.",
             "real": ["Parar o que está fazendo para começar outra coisa custa muito mais do que parece.",
                      "Mesmo um programa bom, se não estava planejado, gera ansiedade."],
             "note": "Não é teimosia. Trocar de tarefa tem um custo real."},
            {"manual": "Rotinas, rituais e padrões rígidos de pensamento.",
             "real": ["Mesmo caminho, mesmo café, mesma ordem de tarefas — todo dia.",
                      "Você precisa saber o plano inteiro antes de sair de casa."],
             "note": "A rotina não é prisão. Para muita gente, é o que torna o dia possível."},
        ],
        "cta": {"comment": "Qual você mais vive: 1, 2 ou 3?", "remember": "Um exemplo sozinho não é diagnóstico."},
        "caption": """Mesmo caminho, mesmo café. É o segundo aspecto do critério B do DSM-5-TR.

Na vida real, pode ser o restaurante mudar o cardápio e o dia sair do eixo. Uma reunião remarcada em cima da hora estragar a tarde. Parar uma tarefa para começar outra custar muito mais do que parece. Precisar saber o plano inteiro antes de sair de casa.

Não é frescura nem teimosia. Para muita gente, a previsibilidade é o que deixa energia para o resto do dia.

Um exemplo sozinho não é diagnóstico. Qual você mais vive: 1, 2 ou 3?

DSM-5-TR, critério B2 (APA, 2022).

{CLOSE}

#DSM5 #rotina #autismoadulto #autismo #TEA""",
    },
]

for _p in POSTS:
    _p["caption"] = _p["caption"].replace("{CLOSE}", CLOSE)
