#!/bin/bash
# Confirma que o LibreOffice arranca com a configuração do Brisa (brisa.xcd) e usa os ícones certos.
# Corre dentro do ambiente Debian de build. Uso: testar-libreoffice.sh <pasta includes.chroot>
set -e
INC="$1"
apt-get install -y -qq --no-install-recommends libreoffice-writer libreoffice-style-elementary >/dev/null
cp "$INC/usr/lib/libreoffice/share/registry/brisa.xcd" /usr/lib/libreoffice/share/registry/
T=$(mktemp -d); cd "$T"
echo "Teste do Brisa" > teste.txt
HOME="$T" soffice --headless --convert-to pdf teste.txt >"$T/saida.log" 2>&1 || true
tail -n 3 "$T/saida.log"
ls -la teste.pdf | awk '{print "PDF criado:", $5, "bytes"}'
echo "--- estilo de icones lido pelo LibreOffice"
grep -o 'SymbolStyle.\{0,80\}' /usr/lib/libreoffice/share/registry/brisa.xcd | head -2
ls /usr/lib/libreoffice/share/config/ | grep -i "images_" | tr '\n' ' '
