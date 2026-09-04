# Posts

One folder per post. The runner publishes one folder a day, cycling through
them in order, so twenty folders is twenty days before anything repeats.

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

## Why the images live in a public repo

Instagram fetches media from a URL — there is no upload. The URL has to be
publicly reachable, so these images cannot live in a private repository. Keep
the images here, in the open, and the tokens somewhere else.

That split is deliberate: the pictures are going onto a public Instagram feed
anyway, and nothing about them is secret. The `.env` is the part that must
never be public.
