#!/bin/bash
# Testa o Brisa 1.0 num ecrã virtual (labwc sem placa gráfica), como sistema instalado e como sessão de instalação.
# Corre dentro do ambiente Debian de build. Uso: testar-10.sh <pasta includes.chroot> <pasta de saída>
set -e
INC="$1"; OUT="$2"; mkdir -p "$OUT"; : > "$OUT/resultado.txt"
apt-get install -y -qq --no-install-recommends labwc waybar grim swaybg fuzzel wlrctl wtype python3-gi gir1.2-gtk-3.0 \
  gir1.2-gtklayershell-0.1 gir1.2-flatpak-1.0 flatpak librsvg2-common librsvg2-bin adwaita-icon-theme papirus-icon-theme \
  fonts-inter fonts-font-awesome fonts-manrope dbus-x11 locales thunar mousepad >/dev/null
sed -i 's/^# *\(pt_PT.UTF-8\|en_US.UTF-8\)/\1/' /etc/locale.gen && locale-gen >/dev/null

cp -r "$INC"/usr/local/bin/. /usr/local/bin/ && chmod 755 /usr/local/bin/brisa-*
rm -rf /usr/share/brisa && mkdir -p /usr/share/brisa && cp -r "$INC"/usr/share/brisa/. /usr/share/brisa/
cp -r "$INC"/usr/share/applications/. /usr/share/applications/
cd /usr/share/brisa/fundos
for svg in *.svg; do
  nome=$(basename "$svg" .svg)
  rsvg-convert -w 1280 -h 800 "$svg" -o "$nome.png"
  rsvg-convert -w 320 -h 200 "$svg" -o "$nome-mini.png"
  cat > desfocar.svg <<EOF
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="800"><defs><filter id="f" x="0" y="0" width="1" height="1"><feGaussianBlur stdDeviation="26"/></filter></defs><image href="$nome.png" x="-140" y="-110" width="1560" height="1020" preserveAspectRatio="xMidYMid slice" filter="url(#f)"/></svg>
EOF
  rsvg-convert desfocar.svg -o "$nome-desfocado.png"
done
rm -f desfocar.svg
cd /

cat > /root/cena10.sh <<'EOF'
#!/bin/sh
r() { echo "[$MODO] $*" >> "$BRISA_OUT/resultado.txt"; }
brisa-fundo &
brisa-barras > /tmp/waybar10-$MODO.log 2>&1 &
brisa-widgets > /tmp/widgets10-$MODO.log 2>&1 &
sleep 4
grim "$BRISA_OUT/$MODO-vazio.png"
pgrep -f "bin/brisa-widgets" >/dev/null && r "widgets: visiveis" || r "widgets: escondidos"
if [ "$MODO" = instalado ]; then
  thunar "$HOME/Documentos" > /dev/null 2>&1 &
  brisa-loja > /dev/null 2>&1 &
  sleep 6
  wlrctl toplevel focus app_id:thunar; sleep 3
  grim "$BRISA_OUT/$MODO-janelas.png"
  pkill thunar; pkill -f brisa-loja; sleep 2
  brisa-apps > /tmp/apps10.log 2>&1 & sleep 4
  grim "$BRISA_OUT/$MODO-aplicacoes.png"; brisa-apps; sleep 2
  brisa-menu > /dev/null 2>&1 & sleep 2
  grim "$BRISA_OUT/$MODO-menu.png"; brisa-menu; sleep 1
fi
pkill -x labwc
EOF
chmod 755 /root/cena10.sh

for MODO in ${MODOS:-instalado instalacao}; do
  H=$(mktemp -d); X=$(mktemp -d); chmod 700 "$X"; mkdir -p "$H/.config" "$H/Documentos"
  cp -r "$INC"/etc/skel/.config/. "$H/.config/"
  sed -i 's/"tray", "wireplumber", //' "$H/.config/waybar/config.jsonc"
  mkdir -p "$H/.config/labwc"
  printf '<?xml version="1.0"?>\n<labwc_config><core><decoration>client</decoration></core></labwc_config>\n' > "$H/.config/labwc/rc.xml"
  for f in "Carta à escola.odt" "Orçamento de novembro.ods" "Lista de compras.txt"; do echo teste > "$H/Documentos/$f"; done
  # Regista os ficheiros como abertos recentemente, para o widget "Continuar onde ficou"
  env -i HOME="$H" PATH=/usr/bin:/bin xvfb-run -a python3 - "$H/Documentos" <<'PY'
import os, sys, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
m = Gtk.RecentManager.get_default()
for f in sorted(os.listdir(sys.argv[1])):
    m.add_item(GLib.filename_to_uri(os.path.join(sys.argv[1], f), None))
GLib.timeout_add(1500, Gtk.main_quit); Gtk.main()
PY
  AO_VIVO=0; [ "$MODO" = instalacao ] && AO_VIVO=1
  env -i HOME="$H" XDG_RUNTIME_DIR="$X" PATH=/usr/local/bin:/usr/bin:/bin LANG=pt_PT.UTF-8 GDK_BACKEND=wayland \
    WLR_BACKENDS=headless WLR_RENDERER=pixman WLR_LIBINPUT_NO_DEVICES=1 BRISA_OUT="$OUT" MODO="$MODO" BRISA_AO_VIVO=$AO_VIVO \
    dbus-run-session -- timeout 90 labwc -s /root/cena10.sh > /tmp/labwc10-$MODO.log 2>&1 || true
done
echo "=== resultados"; cat "$OUT/resultado.txt"
for m in instalado instalacao; do
  echo "=== waybar $m"; grep -i "error\|warn\|critical" /tmp/waybar10-$m.log | grep -vi "a11y\|SYSTEM Bus\|portal" | head -6 | cut -c1-200
  echo "=== widgets $m"; grep -vi "dbind\|a11y\|^$" /tmp/widgets10-$m.log | head -6 | cut -c1-200
done
ls "$OUT"
