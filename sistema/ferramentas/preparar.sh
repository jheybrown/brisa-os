#!/bin/bash
# Prepara o ambiente de build (corre dentro do chroot): instala o live-build e
# extrai os pacotes do Wayfire e do Waybar para consulta das opções de configuração.
set -e
apt-get update -qq
apt-get install -y -qq --no-install-recommends live-build debootstrap squashfs-tools xorriso \
  grub-efi-amd64-bin grub-pc-bin mtools dosfstools isolinux syslinux-common librsvg2-bin \
  fonts-manrope cpio curl ca-certificates rsync >/dev/null
mkdir -p /root/ref && cd /root/ref
apt-get download wayfire waybar >/dev/null 2>&1
for f in *.deb; do dpkg-deb -x "$f" x; done
echo "--- plugins do Wayfire"
ls x/usr/share/wayfire/metadata/ | tr '\n' ' '
echo; echo "--- sessoes"
find x -name '*.desktop' | head
echo "--- lb"; lb --version
