# Carousel formats

`anova.autismo` has three carousel looks. Each topic is assigned one. Claude
writes the slide text, the references and `caption.txt`. The owner lays out the
slides, in Claude Desktop's design option or the usual editor, and drops the
finished folder in `entrada/`.

All three use the same structure: 1080×1350 px, five slides (cover, three body
slides, CTA), a reference on every factual claim, and `@anova.autismo` on every
slide.

Since 2026-10-21, `tools/slides/render.py` renders all three here from the
texts in `tools/slides/posts.py`; see `tools/slides/README.md`. Posts 55–64
were made this way. The DSM-5 posts use the post-39 layout rather than the
white-and-gold one from `gerar_posts.py`.

## House — white and gold

The look of posts 1–30, from `tools/gerar_posts.py`: white `#FFFFFF`, text
`#1E1E24`, gold `#C9A227` headings, gray `#6B6B70`, and the rainbow stripe.
**Use it for** series that already exist in this look, such as the DSM-5
criteria (post 39) and the support levels (40–43).

## A — "Precisamos falar" (photo, serious)

Based on the @renatautista.psi reference.

- **Cover:** a full-bleed photo of one person, looking calm or tired, never in
  crisis. A navy gradient covers the bottom 45% (`#0B1F3A` at 0%, then 90%
  opacity). The headline is two lines of heavy upper-case sans, white. The key
  phrase sits on a yellow block, `#F7C700`, with navy text. One small line
  below it is upper case, with **bold** on one or two words. `@anova.autismo`
  sits at the bottom left and a thin arrow at the bottom right.
- **Body slides:** the same navy, `#0B1F3A`, as a solid background with
  white text. The yellow block marks one phrase per slide, no more. The
  reference goes small at the bottom.
- **Photos:** use your own photos, licensed stock, or generated people. Never
  take a real person's face from the internet.
- **Use it for** heavy topics, which a playful look would trivialise:
  meltdown and shutdown, autistic inertia, interoception, suicide.

## B — "Conheça" (playful, for questions)

Based on the reference with TV characters.

- **Cover:** a cream background, `#FFF6EC`, with pastel blobs in pink,
  `#FFD6E0`, mint, `#CDEFE3`, and sky blue, `#D6E9FF`. Scribbles and a light
  bulb add accents. The headline is a question in rounded heavy sans across
  three lines, with each key word on its own pill: pink `#E5366B`, blue
  `#2E6FD9`, white text. Illustrated people go at the bottom.
- **Body slides:** cream background, one answer per slide, with a small
  illustration.
- **What not to copy from the reference:**
  - **TV stills.** They are copyrighted, and the actors' images are not ours.
    Some of those characters were never written as autistic. Use original
    illustrations.
  - **Puzzle pieces.** Many autistic adults read them as "something missing".
    That runs against the rule that autism is not described as a deficit.
    Use the infinity loop or plain shapes instead.
- **Use it for** factual questions with a short answer: "Autismo é genético?",
  "Quantas pessoas são autistas?", "O que é ecolalia?".

## Posts 55–75

| # | Topic | Format |
| :--- | :--- | :--- |
| 55 | DSM-5 A2: non-verbal communication | DSM (post 39) |
| 56 | Meltdown and shutdown | A |
| 57 | Autismo é genético? | B |
| 58 | DSM-5 A3: relationships | DSM (post 39) |
| 59 | Autistic inertia | A |
| 60 | Quantas pessoas são autistas? | B |
| 61 | DSM-5 B1: repetitive movements and speech | DSM (post 39) |
| 62 | Interoception | A |
| 63 | O que é ecolalia? | B |
| 64 | DSM-5 B2: insistence on sameness | DSM (post 39) |
| 65 | O autismo de antigamente (history of the diagnosis) | A |
| 66 | DSM-5 B3: intense interests | DSM (post 39) |
| 67 | Telas causam autismo? | B |
| 68 | DSM-5 B4: sensory reactivity | DSM (post 39) |
| 69 | Autism and epilepsy | A |
| 70 | O que é o M-CHAT? | B |
| 71 | Autismo tem cura? | B |
| 72 | O que é a CIPTEA? | B |
| 73 | Autism and depression | A |
| 74 | Começar cedo faz diferença? | B |
| 75 | Monotropism | A |

Posts 56, 57 and 60 also exist as reels: `video_meltdown_e_shutdown`,
`video_autismo_e_genetico` and `video_quantas_pessoas_sao_autistas`; so do
59, 62, 65, 67, 71 and 74 (made 2026-11-06).

## Suicide: only under these conditions

The literature supports this topic: suicide mortality is several times higher
in autistic people (Hirvikoski et al., 2016). It gets written only under
these conditions:

- Follow the safe-messaging guidelines (WHO, 2023): no method, no detail of an
  individual case, and no presenting suicide as a solution or as inevitable.
- CVV **188** on the cover and the CTA, and in the caption.
- The DMs it brings stay with a person. The distress pattern in
  `secretary/replies.py` already routes them to the report.

## Prompt for the design tool

Paste the format section above, then:

> Monte um carrossel de 5 slides, 1080×1350, no formato [A/B] descrito acima,
> com exatamente este texto — não reescreva, não acrescente dados:
> [texto dos slides]
> Exporte como slide-01.png … slide-05.png.
