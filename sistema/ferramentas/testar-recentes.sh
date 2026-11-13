#!/bin/bash
# Verifica se os ficheiros registados como recentes chegam ao widget "Continuar onde ficou".
H=$(mktemp -d); mkdir -p "$H/Documentos"; echo t > "$H/Documentos/Carta.odt"; echo t > "$H/Documentos/Contas.ods"
cat > /tmp/rec.py <<'PY'
import os, sys, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
pasta = sys.argv[1]
m = Gtk.RecentManager.get_default()
for f in sorted(os.listdir(pasta)):
    print('add_item', f, m.add_item(GLib.filename_to_uri(os.path.join(pasta, f), None)))
GLib.timeout_add(1500, Gtk.main_quit); Gtk.main()
PY
env -i HOME="$H" PATH=/usr/bin:/bin xvfb-run -a python3 /tmp/rec.py "$H/Documentos" 2>&1 | grep -v Warning
ls -la "$H/.local/share/" 2>&1 | grep recent
cat > /tmp/ler.py <<'PY'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
itens = Gtk.RecentManager.get_default().get_items()
print('itens:', [(i.get_display_name(), i.is_local(), i.exists()) for i in itens])
PY
env -i HOME="$H" PATH=/usr/bin:/bin xvfb-run -a python3 /tmp/ler.py 2>&1 | grep -v Warning
