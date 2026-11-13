#!/bin/bash
# Testa a versão 0.5 num ecrã virtual (compositor labwc sem placa gráfica).
# Corre dentro do ambiente Debian de build. Uso: testar-05.sh <pasta includes.chroot> <pasta de saída>
set -e
INC="$1"; OUT="$2"; mkdir -p "$OUT"
apt-get install -y -qq --no-install-recommends labwc waybar grim swaybg fuzzel wlrctl python3-gi gir1.2-gtk-3.0 \
  gir1.2-flatpak-1.0 flatpak librsvg2-common librsvg2-bin adwaita-icon-theme papirus-icon-theme fonts-inter \
  fonts-font-awesome fonts-manrope dbus-x11 locales thunar mousepad galculator libreoffice-calc libreoffice-gtk3 \
  firefox-esr >/dev/null
sed -i 's/^# *\(pt_PT.UTF-8\|en_US.UTF-8\)/\1/' /etc/locale.gen && locale-gen >/dev/null

cp -r "$INC"/usr/local/bin/. /usr/local/bin/ && chmod 755 /usr/local/bin/brisa-*
mkdir -p /usr/share/brisa && cp -r "$INC"/usr/share/brisa/. /usr/share/brisa/
cp -r "$INC"/usr/share/applications/. /usr/share/applications/
cd /usr/share/brisa/fundos
for nome in rede sinal; do
  rsvg-convert -w 1280 -h 800 "$nome.svg" -o "$nome.png"
  cat > desfocar.svg <<EOF
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="800"><defs><filter id="f" x="0" y="0" width="1" height="1"><feGaussianBlur stdDeviation="26"/></filter></defs><image href="$nome.png" x="-60" y="-40" width="1400" height="880" preserveAspectRatio="xMidYMid slice" filter="url(#f)"/></svg>
EOF
  rsvg-convert desfocar.svg -o "$nome-desfocado.png"
done
rm -f desfocar.svg; cp rede-desfocado.png "$OUT/"
cd /

cat > /root/cena05.sh <<'EOF'
#!/bin/sh
r() { echo "$*" >> "$BRISA_OUT/resultado.txt"; }
brisa-fundo &
brisa-barras > /tmp/waybar05.log 2>&1 &
sleep 3
thunar & mousepad & galculator & brisa-loja > /tmp/loja05.log 2>&1 &
libreoffice --calc & firefox-esr --new-instance about:blank > /tmp/ff05.log 2>&1 &
sleep 30
for id in thunar Thunar org.xfce.mousepad mousepad galculator brisa-loja libreoffice-calc libreoffice-startcenter soffice firefox-esr firefox; do
  if wlrctl toplevel find "app_id:$id"; then r "janela existe: $id"; fi
done
sleep 3
grim "$BRISA_OUT/doca-aberta.png"
# Botões semáforo: traz o Thunar para a frente e fotografa
wlrctl toplevel focus app_id:thunar 2>/dev/null || wlrctl toplevel focus app_id:Thunar 2>/dev/null
sleep 1; grim "$BRISA_OUT/janela.png"
pkill thunar; pkill mousepad; pkill galculator; pkill -f brisa-loja; pkill -f soffice; pkill -f firefox-esr
sleep 3
# Ecrã de Aplicações: abre, fotografa, clica numa zona vazia e confirma que fechou
brisa-apps > /tmp/apps05.log 2>&1 &
sleep 4
grim "$BRISA_OUT/aplicacoes.png"
pgrep -f "bin/brisa-apps" >/dev/null && r "aplicacoes: aberto" || r "aplicacoes: NAO abriu"
wlrctl pointer move -3000 -3000; wlrctl pointer move 1262 400; sleep 1
wlrctl pointer click left; sleep 2
pgrep -f "bin/brisa-apps" >/dev/null && r "aplicacoes: continua aberto depois do clique fora" || r "aplicacoes: fechou com clique fora"
# Segundo pedido fecha (botão da doca outra vez)
brisa-apps > /dev/null 2>&1 & sleep 3; brisa-apps; sleep 2
pgrep -f "bin/brisa-apps" >/dev/null && r "aplicacoes: segundo clique NAO fechou" || r "aplicacoes: segundo clique fecha"
# Menu Brisa: abre por baixo do botão e fecha com segundo clique
brisa-menu > /dev/null 2>&1 & sleep 2
grim "$BRISA_OUT/menu.png"
pgrep -x fuzzel >/dev/null && r "menu: aberto" || r "menu: NAO abriu"
brisa-menu; sleep 1
pgrep -x fuzzel >/dev/null && r "menu: segundo clique NAO fechou" || r "menu: segundo clique fecha"
pkill -x labwc
EOF
chmod 755 /root/cena05.sh

rm -f "$OUT/resultado.txt"
H=$(mktemp -d); X=$(mktemp -d); chmod 700 "$X"; mkdir -p "$H/.config"
cp -r "$INC"/etc/skel/.config/. "$H/.config/"
sed -i 's/"tray", "wireplumber", //' "$H/.config/waybar/config.jsonc"
env -i HOME="$H" XDG_RUNTIME_DIR="$X" PATH=/usr/local/bin:/usr/bin:/bin LANG=pt_PT.UTF-8 \
  WLR_BACKENDS=headless WLR_RENDERER=pixman WLR_LIBINPUT_NO_DEVICES=1 BRISA_OUT="$OUT" GDK_BACKEND=wayland \
  dbus-run-session -- timeout 150 labwc -s /root/cena05.sh > /tmp/labwc05.log 2>&1 || true
echo "=== resultados"; cat "$OUT/resultado.txt"
echo "=== waybar"; grep -i "error\|warn" /tmp/waybar05.log | grep -vi "a11y\|SYSTEM Bus\|portal" | head -8 | cut -c1-200
echo "=== loja"; grep -vi "dbind\|a11y\|^$" /tmp/loja05.log | head -5 | cut -c1-200
echo "=== aplicacoes"; grep -vi "dbind\|a11y\|^$" /tmp/apps05.log | head -5 | cut -c1-200
ls "$OUT"
