#!/usr/bin/env bash
# Serves media/ from this VPS as https://autismo.anovasaude.org/media/, with
# the right Content-Type for video.
#
# Why this exists: Instagram fetches a reel from a URL and reads the
# Content-Type it comes back with. raw.githubusercontent.com returns
# application/octet-stream with nosniff for every file, so a reel hosted there
# fails inside Meta's ingest — minutes later, long after the run has finished.
# Images are unaffected and stay on GitHub.
#
# Run once, as root:  sudo tools/serve-media.sh
# Undo:               sudo tools/serve-media.sh --undo
set -euo pipefail

REPO="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
MEDIA="$REPO/media"
MOUNT=/var/www/media
UNIT=/etc/systemd/system/var-www-media.mount
SITE=/etc/nginx/sites-available/autismosaude
HOST=autismo.anovasaude.org

if [ "${1:-}" = "--undo" ]; then
  systemctl disable --now var-www-media.mount || true
  rm -f "$UNIT"
  systemctl daemon-reload
  echo "Mount removed. Take the 'location /media/' block out of $SITE by hand,"
  echo "then: nginx -t && systemctl reload nginx"
  exit 0
fi

[ "$(id -u)" = 0 ] || { echo "run as root" >&2; exit 1; }

# 1. The repo sits under /root (0700) and nginx runs as www-data, which cannot
#    traverse it. A read-only bind mount exposes just media/ — the same files,
#    so a git pull is visible immediately and there is no copy to keep in step.
mkdir -p "$MOUNT"
cat > "$UNIT" <<EOF
[Unit]
Description=Public media for the Instagram secretary

[Mount]
What=$MEDIA
Where=$MOUNT
Type=none
Options=bind,ro

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now var-www-media.mount
findmnt -n "$MOUNT" >/dev/null || { echo "bind mount failed" >&2; exit 1; }

# 2. One location block, ahead of the proxy to the app on :8001. nginx reads
#    /etc/nginx/mime.types, which already maps mp4 and mov.
if grep -q "location /media/" "$SITE"; then
  echo "nginx already serves /media/ — leaving $SITE alone"
else
  cp "$SITE" "$SITE.bak-$(date +%F)"
  python3 - "$SITE" <<'PY'
import re, sys
path = sys.argv[1]
conf = open(path, encoding="utf-8").read()
block = """
    # The Instagram media, served for Meta's fetcher: reels need a real
    # video/mp4 Content-Type, which raw.githubusercontent.com does not give.
    # Read-only bind mount of the repo's media/ (var-www-media.mount).
    location /media/ {
        alias /var/www/media/;
        autoindex off;
        add_header Cache-Control "public, max-age=3600";
        access_log off;
    }

    location / {"""
conf = conf.replace("\n    location / {", block, 1)
open(path, "w", encoding="utf-8").write(conf)
PY
fi

nginx -t
systemctl reload nginx

# 3. Prove it before trusting it with a post.
echo
echo "Checking what Instagram would see:"
curl -sI "https://$HOST/media/anova.autismo/post-01-autismo-nao-tem-cara/slide-01.png" \
  | grep -i "^HTTP\|^content-type" || true
echo
echo "Now add this line to .env, then reels publish from here:"
echo "  IG_VIDEO_BASE=https://$HOST"
