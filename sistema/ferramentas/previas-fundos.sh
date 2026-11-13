#!/bin/bash
# Converte os fundos SVG em prévias PNG (corre dentro do ambiente Debian de build).
# Uso: previas-fundos.sh <pasta com os .svg> <pasta de saída>
set -e
mkdir -p "$2"
for svg in "$1"/*.svg; do
  nome=$(basename "$svg" .svg)
  rsvg-convert -w 1280 -h 800 "$svg" -o "$2/fundo-$nome.png"
  echo "$nome"
done
