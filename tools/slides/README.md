# Slides

`render.py` turns the texts in `posts.py` into 1080×1350 carousels and a 1080×1920
story per post. `reel.py` turns a rendered carousel into a 9:16 reel with no
music. The three looks are described in `docs/formatos.md`.

```bash
python3 tools/slides/render.py 65             # one post → media/anova.autismo/post-65-…/ + story-65-….png
python3 tools/slides/render.py --out /tmp/x   # preview somewhere else
python3 tools/slides/reel.py 65               # → media/anova.autismo/video_<slug>.mp4 (+ .txt, .jpg)
```

It needs Playwright's `chrome-headless-shell` (already in `~/.cache/ms-playwright`) and `ffmpeg`.

- **Fonts:** Lato, Montserrat, Baloo 2, Nunito and Work Sans, from Google Fonts, under the SIL Open Font License.
- **Illustrations:** Microsoft Fluent Emoji, MIT licence.
- **Logo:** cut from the owner's slides.

A cover in the `foto` format takes `"photo": "file.jpg"` (from `assets/`) in place of the drawn motif.

Never re-render a slide the owner supplied or one that has already been published.
