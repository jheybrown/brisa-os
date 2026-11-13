#!/bin/bash
# Converte todos os SVG de uma pasta em PNG (corre dentro do ambiente Debian de build).
set -e
cd "$1"
for f in *.svg; do
  rsvg-convert "$f" -o "${f%.svg}.png"
  echo "$f"
done
