---
description: Create a new carousel for anova.autismo or pankeka.app, in the house style
---

Create a new post folder following the conventions already in this repo.

**Read first:** `tools/gerar_posts.py` — the `POSTS` list holds the text and
the reference for all twenty existing carousels. Match that voice. Read two or
three entries before writing anything.

Topic and account: $ARGUMENTS

## The shape

Five slides, always: cover, three body slides, CTA. That is what the template
in `tools/gerar_posts.py` renders and what the audience now expects.

- **cover** — one short line, upper case, under 40 characters. A claim or a
  question, never a label.
- **body ×3** — one idea each. A `head` in gold plus `body` text when the idea
  needs a label; body alone when it does not.
- **cta** — the standard final slide. Pass a short note when the topic gives
  it a natural lead-in, otherwise `None`.

## The rules that matter

**Every factual claim carries its `ref`.** Prevalence, sex ratios, diagnostic
criteria, anything with a number — name the source as the existing posts do
(`DSM-5-TR (APA, 2022)`, `Baron-Cohen et al. (2001)`, `CDC, ADDM Network
(2025)`). A claim you cannot source is a claim to cut, not to soften.

**Screening is not diagnosis, and the post must never blur that.** No copy
that implies the test diagnoses, or that a result means someone is autistic.

**No individual clinical advice.** Point to the screening and to professional
assessment. Never tell a reader what their situation is.

**Do not describe autism as illness, deficit or something to cure.**

## Then the caption

Write `caption.txt` in the new folder: a hook echoing the cover, two or three
short paragraphs, then the standard close used by every existing caption
(rastreio gratuito, link na bio, 8 minutos, the não-é-diagnóstico line), then
four hashtags. Read an existing `caption.txt` and match it exactly.

## Finally

Add the post to the `POSTS` list in `tools/gerar_posts.py` so the slides can be
regenerated. The images themselves have to be rendered on the Windows machine
that has the logos and Segoe UI — say so rather than trying to produce PNGs
here.

Show me the slide text and the caption before writing any file.
