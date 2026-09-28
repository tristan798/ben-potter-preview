#!/usr/bin/env bash
# Puts the mail function live on Vercel. Run `npx vercel login` first.
#
# The site itself can stay on GitHub Pages: this deployment exists so that
# POST /api/lead has somewhere to run, and the function sends CORS headers so the
# GitHub Pages origin is allowed to call it.
set -euo pipefail
cd "$(dirname "$0")/.."

V="npx --yes vercel@latest"

if ! $V whoami >/dev/null 2>&1; then
  echo "Not logged in. Run:  npx vercel login"
  exit 1
fi
echo "Logged in as: $($V whoami 2>/dev/null | tail -1)"

$V link --yes --project ben-potter >/dev/null
echo "Project linked."

need() {
  local name="$1" value="$2"
  if $V env ls production 2>/dev/null | grep -q "^ *$name "; then
    echo "  $name already set, leaving it alone"
  else
    printf '%s' "$value" | $V env add "$name" production >/dev/null
    echo "  $name set"
  fi
}

: "${RESEND_API_KEY:?export RESEND_API_KEY before running}"
: "${MAIL_FROM:?export MAIL_FROM, e.g. \"Ben Potter <ben@ben-potter.com>\"}"
: "${LEAD_TO:?export LEAD_TO, e.g. ben.potter@harcourts.co.nz}"

echo "Environment:"
need RESEND_API_KEY "$RESEND_API_KEY"
need MAIL_FROM      "$MAIL_FROM"
need LEAD_TO        "$LEAD_TO"
need ALLOWED_ORIGINS "https://tristan798.github.io,https://ben-potter.com,https://www.ben-potter.com"

echo "Deploying..."
$V deploy --prod --yes
echo
echo "Now set FORM_PROVIDER = \"endpoint\" and FORM_ENDPOINT = \"<that url>/api/lead\""
echo "in tools/content.py, then run: python3 build.py"
