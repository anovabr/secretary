#!/usr/bin/env bash
# Wrapper for cron: loads the credentials, runs the routine, keeps the report.
#
#   tools/run-secretary.sh            # the morning run
#   tools/run-secretary.sh --hourly   # messages and comments only
#   tools/run-secretary.sh --dry-run  # writes nothing
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."

# New posts arrive by push; pull them before deciding what to publish.
git pull --ff-only --quiet || echo "$(date -Is)  git pull falhou; usando o que está em disco" >&2

if [ ! -f .env ]; then
  echo "$(date -Is)  .env não encontrado em $(pwd)" >&2
  exit 1
fi

# shellcheck disable=SC1091
set -a; . ./.env; set +a

mkdir -p reports
REPORT="reports/$(date +%F).txt"

# Each run appends, so the hourly checks accumulate under the morning report
# and the whole day reads as one document.
{
  echo
  echo "═══ $(date '+%H:%M') ═══"
  python3 -m secretary.cli run "$@"
} >> "$REPORT" 2>&1

# The morning run e-mails the report (needs SMTP_PASSWORD in .env; silent
# without it). Hourly checks and dry runs only append to the file.
case " $* " in
  *" --hourly "*|*" --dry-run "*) ;;
  *) python3 -m secretary.deliver "$REPORT" || echo "$(date -Is)  envio do relatório falhou" >> "$REPORT" ;;
esac

cat "$REPORT"
