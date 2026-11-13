#!/bin/bash
# Testa a barra, a doca, a Loja e as Definições num ecrã virtual, em português e em inglês.
# Corre dentro do ambiente Debian de build. Uso: testar-ambiente.sh <pasta includes.chroot> <pasta de saída>
# Usa o compositor labwc sem placa gráfica (o Wayfire precisa de OpenGL e não corre aqui).
set -e
INC="$1"; OUT="$2"; mkdir -p "$OUT"
apt-get install -y -qq --no-install-recommends labwc waybar grim swaybg python3-gi gir1.2-gtk-3.0 \
  librsvg2-common librsvg2-bin adwaita-icon-theme fonts-manrope dbus-x11 locales >/dev/null
apt-get install -y -qq --no-install-recommends wlrctl >/dev/null 2>&1 || echo 'AVISO: sem wlrctl, o teste de passar o rato nao corre'
sed -i 's/^# *\(pt_PT.UTF-8\|en_US.UTF-8\)/\1/' /etc/locale.gen && locale-gen >/dev/null

# Instala os ficheiros do Brisa neste ambiente, como ficariam na imagem
cp -r "$INC"/usr/local/bin/. /usr/local/bin/ && chmod 755 /usr/local/bin/brisa-*
mkdir -p /usr/share/brisa && cp -r "$INC"/usr/share/brisa/. /usr/share/brisa/
for svg in /usr/share/brisa/fundos/*.svg; do
  nome=$(basename "$svg" .svg)
  rsvg-convert -w 1280 -h 800 "$svg" -o "/usr/share/brisa/fundos/$nome.png"
  rsvg-convert -w 320 -h 200 "$svg" -o "/usr/share/brisa/fundos/$nome-mini.png"
  cp "/usr/share/brisa/fundos/$nome.png" "$OUT/fundo-$nome.png"
done
rsvg-convert -w 384 -h 384 /usr/share/brisa/icones/ficheiros.svg -o "$OUT/icone-ficheiros.png"
for f in /usr/local/bin/brisa-loja /usr/local/bin/brisa-definicoes /usr/local/bin/brisa-barras; do python3 -m py_compile "$f"; done
for f in /usr/local/bin/brisa-menu /usr/local/bin/brisa-instalar /usr/local/bin/brisa-lancador /usr/local/bin/brisa-sessao; do sh -n "$f"; done
echo "sintaxe dos programas: ok"

cat > /root/cena.sh <<'EOF'
#!/bin/sh
# Corre dentro do compositor: abre tudo e tira a captura
brisa-fundo &
brisa-barras > /tmp/waybar-$BRISA_L.log 2>&1 &
sleep 2
grim "$BRISA_OUT/barras-$BRISA_L.png"
# Passa o rato por cima do ícone dos Ficheiros: deve crescer e mostrar o nome
if command -v wlrctl >/dev/null; then wlrctl pointer move 372 572; sleep 2; grim "$BRISA_OUT/rato-$BRISA_L.png"; wlrctl pointer move -372 -400; fi
brisa-loja > /tmp/loja-$BRISA_L.log 2>&1 &
sleep 1
brisa-definicoes > /tmp/defs-$BRISA_L.log 2>&1 &
sleep 4
grim "$BRISA_OUT/ambiente-$BRISA_L.png"
pkill -x labwc
EOF
chmod 755 /root/cena.sh

for L in pt en; do
  [ "$L" = pt ] && LOC=pt_PT.UTF-8 || LOC=en_US.UTF-8
  H=$(mktemp -d); X=$(mktemp -d); chmod 700 "$X"; mkdir -p "$H/.config"
  cp -r "$INC"/etc/skel/.config/. "$H/.config/"
  # Neste ambiente não há serviço de som nem bandeja; esses módulos fariam o Waybar parar
  sed -i 's/"tray", "wireplumber", //' "$H/.config/waybar/config.jsonc"
  env -i HOME="$H" XDG_RUNTIME_DIR="$X" PATH=/usr/local/bin:/usr/bin:/bin LANG=$LOC \
    WLR_BACKENDS=headless WLR_RENDERER=pixman WLR_LIBINPUT_NO_DEVICES=1 BRISA_L=$L BRISA_OUT="$OUT" \
    dbus-run-session -- timeout 40 labwc -s /root/cena.sh > /tmp/labwc-$L.log 2>&1 || true
  echo "=== $L: captura"; ls -la "$OUT/ambiente-$L.png" 2>&1 | awk '{print $5, $9}'
  echo "--- waybar ($L): erros e avisos"; grep -i "error\|warn\|critical" /tmp/waybar-$L.log | grep -vi "a11y\|SYSTEM Bus" | cut -c1-220 | head -12
  echo "--- waybar ($L): fim do registo"; tail -n 4 /tmp/waybar-$L.log | cut -c1-220
  echo "--- loja ($L)"; grep -vi "dbind\|a11y\|accessibility" /tmp/loja-$L.log | cut -c1-200 | head -5
  echo "--- definicoes ($L)"; grep -vi "dbind\|a11y\|accessibility" /tmp/defs-$L.log | cut -c1-200 | head -5
done
