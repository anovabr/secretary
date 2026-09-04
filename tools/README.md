# gerar_posts.py

Generates the 100 slides in `media/anova.autismo/` — 20 carousels, five slides
each, 1080x1350. The slide text for every post lives in the `POSTS` list at the
bottom of the file, with its scientific reference where it makes a factual
claim. **Edit the text there and re-run; do not retouch the PNGs.**

It runs on the Windows machine it was written for, and only there:

- fonts are read from `C:\Windows\Fonts` (Segoe UI)
- the logos come from a sibling folder, `Luis - logos/`, which is not in this
  repository

So it is kept here as the source of the images and the record of their
wording, not as something the VPS runs. Making it portable would mean bundling
the logos and falling back to a font that ships with Linux — worth doing only
if the slides need regenerating away from that machine.

Output goes to `posts-imagens/`, which is then copied into `media/<handle>/`.
