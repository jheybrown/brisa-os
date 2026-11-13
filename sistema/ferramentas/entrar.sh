#!/bin/bash
# Corre um comando dentro do ambiente Debian 13 de build (chroot em /opt/brisa/trixie, no WSL).
# Uso, como root no WSL:  entrar.sh <comando> [argumentos...]
set -e
R=/opt/brisa/trixie
for d in proc sys dev dev/pts; do
  mountpoint -q "$R/$d" || mount --bind "/$d" "$R/$d"
done
cat /etc/resolv.conf > "$R/etc/resolv.conf"
exec chroot "$R" /usr/bin/env -i HOME=/root TERM=xterm \
  PATH=/usr/sbin:/usr/bin:/sbin:/bin DEBIAN_FRONTEND=noninteractive "$@"
