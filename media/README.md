# Posts

One folder per post. The runner publishes one a day as a queue: the first
entry that has never gone out, in name order, with a waiting reel after every
two carousels. Only when everything has gone out once does it come back round,
oldest publication first. What went out, and when, is kept in
`.secretary-published.json` beside this folder (on the VPS, not in git), so
adding a folder never reshuffles the rest — it simply joins the queue.

Nothing declares what kind of post a folder is — the files decide. A folder
with a video is a reel, a folder with several images is a carousel, a folder
with one image is a single post.

```
media/
  anova.autismo/
    01-rotina-visual/
      1.png
      2.png
      3.png
      caption.txt
    02-sinais-precoces/
      ...
  pankeka.app/
    01-modo-offline/
      ...
```

**Images** are published in filename order, so name them `1`, `2`, `3`. Two to
ten per folder — that is Instagram's carousel limit. A folder with a single
image is published as a normal post rather than a carousel.

**caption.txt** is the caption, exactly as it should appear, hashtags and all.
A folder with no caption.txt is published without one.

**Folder names** set the order. Prefix them with a number.

## Reels

Drop the video in and it joins the queue as a reel — no
separate list, no change to the board. Loose beside the post folders, exactly
as the editor exports it:

```
media/
  anova.autismo/
    post-31-autismo-mulheres-artigo/      # a carousel, as always
      slide-01.png ...
      caption.txt
    Reel - Autismo - Artigo Luis.mp4      # a reel
    Reel - Autismo - Artigo Luis.txt      # its caption   (optional)
    Reel - Autismo - Artigo Luis.jpg      # its cover     (optional)
```

**The caption and cover are siblings sharing the video's name**, so renaming
the video means renaming all three. Without a caption it publishes bare;
without a cover Instagram picks a frame and the report says so.

**Spaces in the filename are fine** — the URL is escaped. Keep the name
stable once it has published.

A reel can also be a folder of its own (`post-NN-slug/reel.mp4`, with
`caption.txt` and `cover.jpg` inside) if you would rather keep them tidy. One
video per folder: a second is a mistake rather than a second post, so the
first wins. Any *other* image in a reel folder is ignored — a reel is never
published as a carousel of its own frames.

**Order.** Reels do not wait for their place in name order: after two
carousels in a row, the next waiting reel goes out.

**What Instagram accepts:** MP4 or MOV, H.264 video and AAC audio, 9:16
(1080×1920), 3 seconds to 15 minutes, under 1 GB. Anything else has to be
converted before it gets here; otherwise the container fails at Meta's end and
the first you hear of it is the report.

**Video takes minutes to ingest, not seconds.** The runner waits for the
container either way — that wait is the only thing standing between a prepared
reel and a lost one.

### Where the video is served from

From GitHub, like the images. The worry was that `raw.githubusercontent.com`
serves `.mp4` as `application/octet-stream` and Meta would refuse it; in
practice the three reels of 27–29 September went through from GitHub URLs,
container FINISHED and published. `IG_VIDEO_BASE` stays as the escape hatch if
that ever changes:

- `sudo tools/serve-media.sh` — serves this folder from the VPS at
  `https://autismo.anovasaude.org/media/`, where nginx sets `video/mp4`.
- Enable GitHub Pages on `anovabr/secretary` and set
  `IG_VIDEO_BASE=https://anovabr.github.io/secretary`. Pages sets the right
  type too, but caps the site at 1 GB — roughly sixty reels.

**Video in git is heavier than images.** Every reel is pulled onto the VPS
each morning and stays in the repo's history for good. Fifteen megabytes a
reel is fine for a while; a hundred reels is not. When that starts to bite,
the videos move out of the repo and `IG_VIDEO_BASE` follows them.

## Stories

Loose images named `story-NN-slug.png` (1080×1920) beside the folders. One goes
out each morning with the post. A story whose name ends with a post's slug —
`story-03-artigo-mascaramento.png` and `post-50-mascaramento/` — announces that
post and goes out only on its day; the others take turns. Stories have no
caption, and the API cannot add a link sticker: a button drawn into the image
is not clickable, so point to the link in the bio instead.

## Why the images live in a public repo

Instagram fetches media from a URL — there is no upload. The URL has to be
publicly reachable, so these images cannot live in a private repository. Keep
the images here, in the open, and the tokens somewhere else.

That split is deliberate: the pictures are going onto a public Instagram feed
anyway, and nothing about them is secret. The `.env` is the part that must
never be public.
