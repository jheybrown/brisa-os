#!/bin/bash
# Mostra a configuração do instalador (Calamares) do Debian, já extraída em /root/ref/cal.
cd /root/ref/cal/x
mostra() { echo "## $1"; grep -v '^\s*#' "$1" | grep . ; }
mostra usr/bin/calamares-install-debian
mostra usr/share/applications/calamares-install-debian.desktop
mostra etc/calamares/branding/debian/branding.desc
for f in welcome users displaymanager packages unpackfs finished; do mostra etc/calamares/modules/$f.conf; done
echo "## show.qml"; head -40 etc/calamares/branding/debian/show.qml
ls etc/calamares/branding/debian/
