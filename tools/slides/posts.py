# -*- coding: utf-8 -*-
"""Textos dos carrosséis 55–75 (anova.autismo), renderizados por render.py.

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
    # ------------------------------------------------------------------ 65
    {
        "n": 65, "slug": "autismo-de-antigamente", "format": "foto", "motif": "timeline",
        "ref": "Volkmar & McPartland (2014), Annu Rev Clin Psychol · Brugha et al. (2011), Arch Gen Psychiatry",
        "cover": {
            "pre": "Precisamos falar sobre",
            "hl": "o autismo de antigamente",
            "sub": "**Ele sempre existiu.** O que faltava era **o nome certo**.",
        },
        "body": [
            {"kicker": "Antes de 1980",
             "text": "Nos manuais de 1952 e 1968, crianças autistas recebiam [[outro rótulo]]: “esquizofrenia infantil”.",
             "more": "O autismo só virou diagnóstico próprio em 1980 — quase 40 anos depois de descrito por Leo Kanner, em 1943."},
            {"kicker": "E os adultos?",
             "text": "Uma pesquisa na Inglaterra encontrou [[cerca de 1% de autistas]] entre adultos — inclusive idosos.",
             "more": "A proporção é parecida com a das crianças. E esses adultos tendiam a passar despercebidos."},
            {"kicker": "Não surgiu agora",
             "text": "A proporção não mudou com a idade: [[sempre houve autistas]].",
             "more": "O que mudou foi a capacidade de reconhecer — nas crianças e, agora, nos adultos."},
        ],
        "cta": {"lead": "Cresceu sem diagnóstico?", "hl": "Vale fazer um rastreio."},
        "caption": """O autismo não é novo. O nome certo é que demorou.

Leo Kanner descreveu o autismo em 1943. Mas, nos manuais de psiquiatria de 1952 e 1968, crianças autistas recebiam outro rótulo: “esquizofrenia infantil”. O autismo só virou diagnóstico próprio em 1980.

E os adultos daquela época? Uma pesquisa na Inglaterra avaliou adultos de todas as idades e encontrou cerca de 1% de autistas — proporção parecida com a das crianças, sem diferença entre jovens e idosos. Esses adultos tendiam a passar despercebidos.

Sempre houve autistas. O que mudou foi a capacidade de reconhecer.

Volkmar & McPartland (2014), Annual Review of Clinical Psychology; Brugha et al. (2011), Archives of General Psychiatry.

{CLOSE}

#historiadoautismo #diagnosticotardio #autismoadulto #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 66
    {
        "n": 66, "slug": "dsm5-interesses-intensos", "format": "dsm",
        "ref": "DSM-5-TR, critério B3 (APA, 2022)",
        "cover": {
            "kicker": "Critério B · Aspecto 3",
            "title": "Interesses fixos e intensos",
            "lead": "Saber tudo sobre uma coisa só.",
            "punch": "Não é só gostar muito. É o assunto ocupar o espaço inteiro.",
        },
        "examples": [
            {"manual": "Interesses fixos e muito restritos, fora do comum na intensidade ou no foco.",
             "real": ["Você passa o fim de semana inteiro lendo sobre trens, fungos ou uma banda — e nem vê a hora passar.",
                      "Numa conversa, sempre encontra um caminho de volta para o seu assunto."],
             "note": "Não é obsessão vazia. Para muita gente, é a maior fonte de prazer e de calma."},
            {"manual": "Forte apego a objetos ou temas incomuns.",
             "real": ["Você coleciona algo que ninguém à sua volta entende — e sabe a história de cada peça.",
                      "Um objeto específico precisa estar com você para o dia dar certo."],
             "note": "O valor não está no objeto. Está no que ele organiza por dentro."},
            {"manual": "Interesses excessivamente circunscritos ou perseverativos.",
             "real": ["Você lê o mesmo livro, assiste à mesma série, ouve a mesma música pela vigésima vez.",
                      "Muda de assunto só quando alguém interrompe — e custa voltar para o resto."],
             "note": "Repetir o que se conhece descansa. O novo cansa mais do que parece."},
        ],
        "cta": {"comment": "Qual é (ou foi) o seu assunto?", "remember": "Um exemplo sozinho não é diagnóstico."},
        "caption": """Interesses fixos e intensos: não é só gostar muito.

É o terceiro aspecto do critério B do DSM-5-TR. Na vida real, pode ser passar o fim de semana inteiro lendo sobre trens, fungos ou uma banda sem ver a hora passar. Sempre achar um caminho de volta para o seu assunto. Colecionar algo que ninguém entende e saber a história de cada peça. Ver a mesma série pela vigésima vez.

Não é obsessão vazia. Para muita gente, é a maior fonte de prazer e de calma do dia.

Um exemplo sozinho não é diagnóstico. Qual é — ou foi — o seu assunto?

DSM-5-TR, critério B3 (APA, 2022).

{CLOSE}

#DSM5 #hiperfoco #autismoadulto #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 67
    {
        "n": 67, "slug": "telas-causam-autismo", "format": "conheca",
        "ref": "Ophir et al. (2023), JAMA Network Open · Bai et al. (2019), JAMA Psychiatry",
        "cover": {
            "lines": [("Telas causam", "plain"), ("autismo?", "pink")],
            "sub": "A resposta curta: as pesquisas não mostram isso.",
            "people": ["woman_technologist-medium", "person_raising_hand-medium", "man_tipping_hand-medium-dark", "teacher-medium-dark"],
        },
        "body": [
            {"kicker": "O que os estudos acharam", "emoji": "bar_chart",
             "head": "[[46 estudos]], 560 mil pessoas",
             "text": "Uma revisão juntou tudo o que havia. A associação entre tela e autismo foi pequena — e deixou de ser significativa depois de corrigido o viés de publicação.",
             "ref": "Ophir et al. (2023), JAMA Network Open"},
            {"kicker": "Pode ser o contrário", "emoji": "mobile_phone",
             "head": "Quem veio [[primeiro]]?",
             "text": "Os estudos eram observacionais. Os autores lembram que crianças autistas podem preferir telas — e não o contrário.",
             "ref": "Ophir et al. (2023), JAMA Network Open"},
            {"kicker": "O que mais pesa", "emoji": "dna",
             "head": "Cerca de [[80%]] é herdado",
             "text": "Num estudo com 2 milhões de pessoas, a maior parte da variação no risco de autismo veio de fatores herdados.",
             "ref": "Bai et al. (2019), JAMA Psychiatry"},
        ],
        "cta": {"lead": "Ficou com dúvida sobre você?", "head": "Faça o rastreio gratuito"},
        "caption": """Telas causam autismo? As pesquisas não mostram isso.

Uma revisão de 2023 juntou 46 estudos, com mais de 560 mil pessoas. A associação entre tempo de tela e autismo foi pequena — e deixou de ser significativa depois de corrigido o viés de publicação. Todos os estudos eram observacionais, e os autores lembram que o caminho pode ser o inverso: crianças autistas podem preferir telas.

O que mais pesa é outra coisa: num estudo com 2 milhões de pessoas, cerca de 80% da variação no risco de autismo veio de fatores herdados.

Tela demais pode trazer outros problemas. Mas culpar a tela, ou os pais, pelo autismo não tem base.

Ophir et al. (2023), JAMA Network Open; Bai et al. (2019), JAMA Psychiatry.

{CLOSE}

#mitosobreautismo #telas #autismo #autismoinfantil #TEA""",
    },
    # ------------------------------------------------------------------ 68
    {
        "n": 68, "slug": "dsm5-sensorial", "format": "dsm",
        "ref": "DSM-5-TR, critério B4 (APA, 2022)",
        "cover": {
            "kicker": "Critério B · Aspecto 4",
            "title": "Reação diferente a sons, luzes, texturas e dor",
            "lead": "Demais ou de menos.",
            "punch": "O mesmo mundo, num volume que não é o dos outros.",
        },
        "examples": [
            {"manual": "Hiper-reatividade a estímulos sensoriais.",
             "real": ["O barulho do liquidificador, da obra ou do restaurante cheio dói de verdade.",
                      "Você corta a etiqueta de toda roupa nova antes de usar."],
             "note": "Não é frescura. O estímulo chega mais alto do que chega para os outros."},
            {"manual": "Hiporreatividade: aparente indiferença a dor ou temperatura.",
             "real": ["Você descobre um machucado horas depois, sem lembrar de quando bateu.",
                      "Sai de casa de manga curta num dia frio e só percebe quando alguém comenta."],
             "note": "Sentir menos também é diferença sensorial — e pode passar despercebido."},
            {"manual": "Interesse incomum por aspectos sensoriais do ambiente.",
             "real": ["Você fica olhando luzes, reflexos ou coisas girando mais tempo do que os outros.",
                      "Precisa cheirar ou tocar um objeto para conhecê-lo de verdade."],
             "note": "Às vezes o sensorial não incomoda: encanta."},
        ],
        "cta": {"comment": "Qual você mais vive: 1, 2 ou 3?", "remember": "Um exemplo sozinho não é diagnóstico."},
        "caption": """Sons, luzes, texturas, dor: o mesmo mundo, num volume diferente.

É o quarto aspecto do critério B do DSM-5-TR. Na vida real, pode ser o barulho do liquidificador doer de verdade. Cortar a etiqueta de toda roupa nova. Descobrir um machucado horas depois. Sair de manga curta no frio e só perceber quando alguém comenta. Ficar olhando luzes e reflexos mais tempo do que os outros.

Pode ser demais, pode ser de menos — e às vezes não incomoda, encanta.

Um exemplo sozinho não é diagnóstico. Qual você mais vive: 1, 2 ou 3?

DSM-5-TR, critério B4 (APA, 2022).

{CLOSE}

#DSM5 #sensorial #autismoadulto #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 69
    {
        "n": 69, "slug": "autismo-e-epilepsia", "format": "foto", "motif": "eeg",
        "ref": "Liu et al. (2022), Autism · Strasser et al. (2018), Dev Med Child Neurol · Hyman et al. (2020), Pediatrics",
        "cover": {
            "pre": "Precisamos falar sobre",
            "hl": "autismo e epilepsia",
            "sub": "**Andam juntos** mais do que se imagina — **e pouca gente sabe**.",
        },
        "body": [
            {"kicker": "Quanto",
             "text": "Juntando 66 estudos, cerca de [[1 em cada 10 autistas]] também tinha epilepsia.",
             "more": "Foi mais comum em adolescentes, adultos, mulheres e em quem tem deficiência intelectual."},
            {"kicker": "Nos dois sentidos",
             "text": "Entre pessoas com epilepsia, [[6,3% eram autistas]].",
             "more": "Em algumas formas de epilepsia infantil, a proporção foi muito maior."},
            {"kicker": "Por que importa",
             "text": "A Academia Americana de Pediatria pede que os médicos [[conheçam as condições]] que acompanham o autismo.",
             "more": "Convulsões estão nessa lista, ao lado de sono, intestino, ansiedade e TDAH."},
        ],
        "cta": {"lead": "Se reconheceu no autismo?", "hl": "Vale fazer um rastreio."},
        "caption": """Autismo e epilepsia andam juntos mais do que se imagina.

Uma revisão de 66 estudos estimou que cerca de 1 em cada 10 autistas também tem epilepsia — mais comum em adolescentes, adultos, mulheres e em quem tem deficiência intelectual.

O caminho inverso também aparece: entre pessoas com epilepsia, 6,3% eram autistas, e em algumas epilepsias da infância a proporção foi bem maior.

Por isso a Academia Americana de Pediatria pede que os médicos conheçam as condições que costumam acompanhar o autismo — convulsões entre elas.

Liu et al. (2022), Autism; Strasser et al. (2018), Developmental Medicine & Child Neurology; Hyman et al. (2020), Pediatrics.

{CLOSE}

#epilepsia #autismo #autismoadulto #neurologia #TEA""",
    },
    # ------------------------------------------------------------------ 70
    {
        "n": 70, "slug": "o-que-e-o-mchat", "format": "conheca",
        "ref": "Robins et al. (2014), Pediatrics · Hyman et al. (2020), Pediatrics · Lei 13.438/2017",
        "cover": {
            "lines": [("O que é o", "plain"), ("M-CHAT?", "blue")],
            "sub": "O rastreio de autismo feito na primeira infância.",
            "people": ["woman_raising_hand-medium-dark", "health_worker-medium-light", "teacher-medium-dark", "man_raising_hand-medium-light"],
        },
        "body": [
            {"kicker": "O que é", "emoji": "writing_hand",
             "head": "Perguntas [[para os pais]]",
             "text": "Um questionário respondido pela família, aplicado nas consultas de 18 e 24 meses. A Academia Americana de Pediatria recomenda o rastreio nessas duas idades.",
             "ref": "Robins et al. (2014); Hyman et al. (2020), Pediatrics"},
            {"kicker": "Rastreio não é diagnóstico", "emoji": "magnifying_glass_tilted_left",
             "head": "[[47,5%]] tiveram diagnóstico",
             "text": "Entre 16 mil crianças, das que seguiram em risco após a entrevista, 47,5% foram diagnosticadas com autismo — e 94,6% tinham algum atraso ou ponto de atenção.",
             "ref": "Robins et al. (2014), Pediatrics"},
            {"kicker": "No Brasil", "emoji": "calendar",
             "head": "É lei [[até os 18 meses]]",
             "text": "Desde 2017, toda criança deve passar por um instrumento de detecção de risco para o desenvolvimento psíquico nos primeiros 18 meses.",
             "ref": "Lei 13.438/2017"},
        ],
        "cta": {"lead": "Tem dúvida sobre seu filho?", "head": "Faça o rastreio gratuito"},
        "caption": """O que é o M-CHAT? É o rastreio de autismo mais usado na primeira infância.

São perguntas respondidas pelos pais nas consultas de 18 e 24 meses — as idades em que a Academia Americana de Pediatria recomenda rastrear.

Rastreio não é diagnóstico, e os números mostram isso: num estudo com 16 mil crianças, das que seguiram em risco depois da entrevista, 47,5% foram diagnosticadas com autismo. Mas 94,6% tinham algum atraso ou ponto de atenção no desenvolvimento — ou seja, quase sempre vale avaliar. E essas crianças foram diagnosticadas dois anos mais cedo do que a mediana nos EUA.

No Brasil, desde 2017 a lei exige um instrumento de detecção de risco para o desenvolvimento psíquico nos primeiros 18 meses de vida.

Robins et al. (2014), Pediatrics; Hyman et al. (2020), Pediatrics; Lei 13.438/2017.

{CLOSE}

#MCHAT #autismoinfantil #rastreio #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 71
    {
        "n": 71, "slug": "autismo-tem-cura", "format": "conheca",
        "ref": "DSM-5-TR (APA, 2022) · Hyman et al. (2020), Pediatrics · FDA (2019)",
        "cover": {
            "lines": [("Autismo", "plain"), ("tem cura?", "pink")],
            "sub": "A pergunta parte de uma ideia errada.",
            "people": ["person_tipping_hand-medium", "woman_gesturing_ok-medium", "health_worker-medium-light", "woman_tipping_hand-medium-light"],
        },
        "body": [
            {"kicker": "O que é", "emoji": "brain",
             "head": "Não é [[doença]]",
             "text": "Autismo é uma forma de o cérebro se desenvolver. Os sinais aparecem desde o início do desenvolvimento.",
             "ref": "DSM-5-TR (APA, 2022)"},
            {"kicker": "O que muda", "emoji": "people_hugging",
             "head": "O que muda é [[o apoio]]",
             "text": "Há intervenções com evidência para trabalhar habilidades específicas — escolhidas junto com a família.",
             "ref": "Hyman et al. (2020), Pediatrics"},
            {"kicker": "Cuidado", "emoji": "warning",
             "head": "Desconfie de [[“cura”]]",
             "text": "O MMS, vendido como cura do autismo, é dióxido de cloro — um alvejante. A FDA alertou: não beba, faz mal.",
             "ref": "FDA (2019)"},
        ],
        "cta": {"lead": "Quer entender o seu caso?", "head": "Faça o rastreio gratuito"},
        "caption": """Autismo tem cura? A pergunta parte de uma ideia errada.

Autismo não é doença. É uma condição do neurodesenvolvimento: uma forma de o cérebro se desenvolver, com sinais desde o início da vida.

O que muda é o apoio. Existem intervenções com evidência para trabalhar habilidades específicas — escolhidas junto com a família, não impostas.

E desconfie de quem vende “cura”. O MMS, oferecido como tratamento para autismo, é dióxido de cloro, um alvejante. A FDA alertou que o produto não deve ser consumido e pode causar danos sérios.

DSM-5-TR (APA, 2022); Hyman et al. (2020), Pediatrics; FDA (2019).

{CLOSE}

#mitosobreautismo #neurodiversidade #autismo #autismoadulto #TEA""",
    },
    # ------------------------------------------------------------------ 72
    {
        "n": 72, "slug": "o-que-e-a-ciptea", "format": "conheca",
        "ref": "Lei 13.977/2020 · Lei 12.764/2012",
        "cover": {
            "lines": [("O que é a", "plain"), ("CIPTEA?", "blue")],
            "sub": "A carteira de identificação da pessoa autista.",
            "people": ["woman_raising_hand-medium-dark", "man_raising_hand-medium-light", "person_raising_hand-medium", "woman_technologist-medium"],
        },
        "body": [
            {"kicker": "O que é", "emoji": "identification_card",
             "head": "Uma carteira [[gratuita]]",
             "text": "Criada em 2020, identifica a pessoa com autismo para garantir atenção integral e prioridade no atendimento, em serviços públicos e privados.",
             "ref": "Lei 13.977/2020"},
            {"kicker": "Como pedir", "emoji": "writing_hand",
             "head": "Com [[relatório médico]]",
             "text": "O pedido é feito ao órgão do estado ou do município, com relatório médico que indique o código da CID.",
             "ref": "Lei 13.977/2020, art. 3º-A, § 1º"},
            {"kicker": "Validade", "emoji": "calendar",
             "head": "Vale [[5 anos]]",
             "text": "Depois é revalidada com o mesmo número — o que também ajuda a contar quantas pessoas autistas há no país.",
             "ref": "Lei 13.977/2020, art. 3º-A, § 3º"},
        ],
        "cta": {"lead": "Ainda não tem diagnóstico?", "head": "Comece pelo rastreio"},
        "caption": """O que é a CIPTEA? É a Carteira de Identificação da Pessoa com Transtorno do Espectro Autista.

Criada pela Lei 13.977/2020, ela serve para garantir atenção integral, pronto atendimento e prioridade no atendimento e no acesso a serviços públicos e privados — principalmente saúde, educação e assistência social. A expedição é gratuita.

O pedido é feito ao órgão responsável do seu estado ou município, com relatório médico que indique o código da CID. A carteira vale 5 anos e é revalidada com o mesmo número.

Os detalhes do pedido mudam de cidade para cidade: vale consultar a prefeitura ou a secretaria de assistência social.

Lei 13.977/2020; Lei 12.764/2012 (Lei Berenice Piana).

{CLOSE}

#CIPTEA #direitosdoautista #autismo #autismoadulto #TEA""",
    },
    # ------------------------------------------------------------------ 73
    {
        "n": 73, "slug": "autismo-e-depressao", "format": "foto", "motif": "cloud",
        "ref": "Hollocks et al. (2019), Psychological Medicine",
        "cover": {
            "pre": "Precisamos falar sobre",
            "hl": "autismo e depressão",
            "sub": "**Não faz parte do autismo.** Mas aparece **muito** junto.",
        },
        "body": [
            {"kicker": "Depressão",
             "text": "Juntando 29 estudos, [[23% dos adultos autistas]] estavam com depressão no momento — e 37% já tinham tido ao longo da vida.",
             "more": "São mais de 26 mil pessoas, em pesquisas de vários países."},
            {"kicker": "Ansiedade",
             "text": "Com a ansiedade, os números foram ainda maiores: [[27% no momento, 42% na vida]].",
             "more": "Os estudos variaram bastante entre si: são estimativas, não um retrato exato."},
            {"kicker": "O que fazer",
             "text": "Depressão e ansiedade [[merecem cuidado próprio]], com profissional de saúde mental.",
             "more": "Se você está em sofrimento agora, ligue 188 (CVV): gratuito, 24 horas."},
        ],
        "cta": {"lead": "Nunca investigou autismo?", "hl": "Vale fazer um rastreio."},
        "caption": """Depressão não faz parte do autismo. Mas aparece muito junto.

Uma revisão de 29 estudos, com mais de 26 mil adultos autistas, estimou que 23% estavam com depressão no momento da pesquisa e 37% já tinham tido ao longo da vida. Com a ansiedade, os números foram ainda maiores: 27% no momento e 42% na vida.

Os estudos variaram bastante entre si, então esses números são estimativas, não um retrato exato.

Depressão e ansiedade merecem cuidado próprio, com profissional de saúde mental. Se você está em sofrimento agora, ligue 188 (CVV): é gratuito e funciona 24 horas.

Hollocks et al. (2019), Psychological Medicine.

{CLOSE}

#depressao #saudemental #autismoadulto #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 74
    {
        "n": 74, "slug": "comecar-cedo-faz-diferenca", "format": "conheca",
        "ref": "Hyman et al. (2020), Pediatrics · Dawson et al. (2010), Pediatrics",
        "cover": {
            "lines": [("Começar cedo", "plain"), ("faz diferença?", "blue")],
            "sub": "Sim — e por isso o rastreio importa.",
            "people": ["teacher-medium-dark", "woman_raising_hand-medium-dark", "health_worker-medium-light", "man_tipping_hand-medium-dark"],
        },
        "body": [
            {"kicker": "Quando", "emoji": "calendar",
             "head": "A partir de [[18 meses]]",
             "text": "O autismo pode ser diagnosticado a partir dos 18 meses — e há intervenções com evidência que podem ajudar.",
             "ref": "Hyman et al. (2020), Pediatrics"},
            {"kicker": "O que um estudo mostrou", "emoji": "bar_chart",
             "head": "[[17,6 pontos]] contra 7,0",
             "text": "Num ensaio com 48 crianças de 18 a 30 meses, dois anos de intervenção precoce trouxeram ganho médio maior em testes cognitivos do que o atendimento comum.",
             "ref": "Dawson et al. (2010), Pediatrics"},
            {"kicker": "Quem participa", "emoji": "people_hugging",
             "head": "[[A família]] junto",
             "text": "No estudo, terapeutas e pais aplicavam a intervenção. As decisões sobre o cuidado devem ser tomadas com a família.",
             "ref": "Dawson et al. (2010); Hyman et al. (2020)"},
        ],
        "cta": {"lead": "Notou sinais no seu filho?", "head": "Faça o rastreio gratuito"},
        "caption": """Começar cedo faz diferença? Sim — e por isso o rastreio importa.

O autismo pode ser diagnosticado a partir dos 18 meses, e há intervenções com evidência que podem ajudar.

Num ensaio clínico com 48 crianças de 18 a 30 meses, as que receberam dois anos de intervenção precoce, aplicada por terapeutas e pelos próprios pais, ganharam em média 17,6 pontos em testes cognitivos. No grupo com atendimento comum, o ganho foi de 7,0.

Não se trata de mudar quem a criança é, e sim de dar apoio no momento em que ele rende mais — com a família participando das decisões.

Hyman et al. (2020), Pediatrics; Dawson et al. (2010), Pediatrics.

{CLOSE}

#intervencaoprecoce #autismoinfantil #rastreio #autismo #TEA""",
    },
    # ------------------------------------------------------------------ 75
    {
        "n": 75, "slug": "monotropismo", "format": "foto", "motif": "beam",
        "ref": "Murray, Lesser & Lawson (2005), Autism",
        "cover": {
            "pre": "Precisamos falar sobre",
            "hl": "monotropismo",
            "sub": "Uma teoria sobre **atenção** que ajuda a entender **o autismo**.",
        },
        "body": [
            {"kicker": "A ideia",
             "text": "A atenção autista tende a se concentrar em [[poucos interesses de cada vez]] — e com muita intensidade.",
             "more": "Como uma lanterna de feixe estreito, e não uma luz que ilumina a sala inteira."},
            {"kicker": "O que explica",
             "text": "Para os autores, as dificuldades sociais e de comunicação [[decorrem desse jeito de distribuir a atenção]].",
             "more": "Conversa em grupo pede atenção espalhada. É justamente o que custa mais."},
            {"kicker": "Quem propôs",
             "text": "A teoria foi escrita por pesquisadores — [[entre eles, uma pessoa autista]].",
             "more": "Parte dela vem da experiência de quem vive o autismo por dentro."},
        ],
        "cta": {"lead": "Sua atenção funciona assim?", "hl": "Vale fazer um rastreio."},
        "caption": """Monotropismo: uma teoria sobre atenção que ajuda a entender o autismo.

A ideia é que a atenção autista tende a se concentrar em poucos interesses de cada vez, com muita intensidade — como uma lanterna de feixe estreito, e não uma luz que ilumina a sala inteira.

Para os autores, isso ajuda a explicar o resto: conversa em grupo, mudança de assunto e interrupções pedem atenção espalhada, que é justamente o que custa mais.

A teoria foi escrita por pesquisadores, entre eles uma pessoa autista, e parte da experiência de quem vive o autismo por dentro. É uma teoria, não um diagnóstico.

Murray, Lesser & Lawson (2005), Autism.

{CLOSE}

#monotropismo #hiperfoco #autismoadulto #autismo #TEA""",
    },
]

for _p in POSTS:
    _p["caption"] = _p["caption"].replace("{CLOSE}", CLOSE)
