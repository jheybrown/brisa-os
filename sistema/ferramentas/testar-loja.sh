#!/bin/bash
# Testa a Loja e as folhas de estilo num ecrã virtual (corre dentro do ambiente Debian de build).
# Uso: testar-loja.sh <pasta config do live-build> <png de saída>
set -e
apt-get install -y -qq --no-install-recommends python3-gi gir1.2-gtk-3.0 xvfb xauth adwaita-icon-theme librsvg2-common >/dev/null
CFG="$1"; PNG="$2"
cat > /tmp/teste_loja.py <<'EOF'
import runpy, sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

cfg, png = sys.argv[1], sys.argv[2]
# 1. As folhas de estilo têm de ser CSS GTK válido
for f in ('etc/skel/.config/waybar/style.css', 'etc/skel/.config/gtk-3.0/gtk.css'):
    Gtk.CssProvider().load_from_path(f'{cfg}/includes.chroot/{f}')
    print('CSS valido:', f)

# 2. A Loja abre, filtra e desenha-se
m = runpy.run_path(f'{cfg}/includes.chroot/usr/local/bin/brisa-loja', run_name='teste')
j = m['Loja']()
j.show_all()

def passo():
    linhas = j.lista.get_children()
    j.busca.set_text('vlc')
    visiveis = [l.nome for l in linhas if j.filtrar(l)]
    assert visiveis == ['VLC'], visiveis
    j.busca.set_text('')
    print('aplicacoes no catalogo:', len(linhas), '| filtro ok')
    GLib.timeout_add(600, captura)
    return False

def captura():
    w = j.get_window()
    Gdk.pixbuf_get_from_window(w, 0, 0, w.get_width(), w.get_height()).savev(png, 'png', [], [])
    print('captura guardada')
    Gtk.main_quit()
    return False

GLib.timeout_add(800, passo)
Gtk.main()
EOF
xvfb-run -a -s "-screen 0 1000x760x24" python3 /tmp/teste_loja.py "$CFG" "$PNG"
