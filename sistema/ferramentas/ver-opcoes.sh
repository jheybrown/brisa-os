#!/bin/bash
# Lista as opções (nome = valor por omissão) dos plugins do Wayfire pedidos.
cd /root/ref/x/usr/share/wayfire/metadata
for p in "$@"; do
  echo "[$p]"
  tr '\n' ' ' < "$p.xml" | grep -oE '<option name="[^"]+" type="[^"]+">.{0,400}?</option>' \
    | sed -E 's/<option name="([^"]+)" type="([^"]+)">.*<default>([^<]*)<\/default>.*/\1 (\2) = \3/; s/<option name="([^"]+)" type="([^"]+)">.*/\1 (\2)/'
done
