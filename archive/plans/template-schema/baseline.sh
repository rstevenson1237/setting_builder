#!/bin/sh
# Phase 0 baseline: what every later phase is diffed against.
#   sh plans/template-schema/baseline.sh DIR    writes the baseline into DIR
#   diff -r plans/template-schema/baseline DIR  checks a phase against it
# The site and PDF are kept as hashes; to see a changed page, rebuild it at this commit.
set -e
out=${1:?usage: baseline.sh DIR}
cd "$(dirname "$0")/../.."
mkdir -p "$out"
tmp=$(mktemp -d)
v=tools/validate_setting.py
steps=$(sed -n 's/^ *- \([0-9][a-z]\)\. .*/\1/p' STEPS.md)
regions=$(ls setting/region | sed -n 's/^\([A-Z]*\)$/\1/p')
: > "$out/read-set.txt"; : > "$out/skeleton.txt"
for s in $steps; do
  for r in "" $regions; do
    { echo "== $s $r"; python3 $v --read-set $s $r 2>&1 || true; } >> "$out/read-set.txt"
    { echo "== $s $r"; python3 $v --skeleton $s $r 2>&1 || true; } >> "$out/skeleton.txt"
  done
done
python3 tools/metrics.py > "$out/metrics.txt" 2>&1
python3 tools/build_site.py --out "$tmp/site" > /dev/null
python3 tools/build_pdf.py --html-out "$tmp/pdf.html" > /dev/null 2>&1 || true
(cd "$tmp/site" && find . -type f | LC_ALL=C sort | xargs sha256sum) > "$out/site.sha256"
(cd "$tmp" && sha256sum pdf.html) > "$out/pdf.sha256"
rm -rf "$tmp"
