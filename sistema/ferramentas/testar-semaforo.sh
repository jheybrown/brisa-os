#!/bin/bash
# Fotografa janelas com a barra de título desenhada pela própria aplicação (como no Wayfire),
# para confirmar os botões semáforo. Corre dentro do ambiente Debian de build, depois de testar-05.sh.
INC="$1"; OUT="$2"
echo "--- entradas secundarias"; ls /usr/share/applications | grep -i "thunar\|mousepad\|foot\|wcm\|settings" | tr '\n' ' '; echo
cat > /root/cena-sem.sh <<'EOF'
#!/bin/sh
brisa-fundo &
sleep 1
GTK_CSD=1 brisa-definicoes > /dev/null 2>&1 &
sleep 2
GTK_CSD=1 thunar /usr > /dev/null 2>&1 &
sleep 5
grim "$BRISA_OUT/semaforo.png"
pkill -x labwc
EOF
chmod 755 /root/cena-sem.sh
H=$(mktemp -d); X=$(mktemp -d); chmod 700 "$X"; mkdir -p "$H/.config"
cp -r "$INC"/etc/skel/.config/. "$H/.config/"
mkdir -p "$H/.config/labwc"
printf '<?xml version="1.0"?>
<labwc_config><core><decoration>client</decoration></core></labwc_config>
' > "$H/.config/labwc/rc.xml"
env -i HOME="$H" XDG_RUNTIME_DIR="$X" PATH=/usr/local/bin:/usr/bin:/bin LANG=pt_PT.UTF-8 \
  WLR_BACKENDS=headless WLR_RENDERER=pixman WLR_LIBINPUT_NO_DEVICES=1 BRISA_OUT="$OUT" GDK_BACKEND=wayland \
  dbus-run-session -- timeout 40 labwc -s /root/cena-sem.sh > /dev/null 2>&1 || true
ls -la "$OUT/semaforo.png" | awk '{print $5, $9}'
