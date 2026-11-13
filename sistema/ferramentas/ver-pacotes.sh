#!/bin/bash
# Mostra a versão disponível no Debian de cada pacote pedido (corre dentro do chroot).
apt-get update -qq 2>&1 | tail -1
for p in "$@"; do
  v=$(apt-cache policy "$p" 2>/dev/null | awk '/Candidate:/ {print $2}')
  printf '%-28s %s\n' "$p" "${v:-(nao existe)}"
done
