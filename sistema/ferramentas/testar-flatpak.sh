#!/bin/bash
# Testa as chamadas à biblioteca do Flatpak que a Loja usa: tamanho, progresso e cancelar.
# Corre dentro do ambiente Debian de build, com Internet.
set -e
apt-get install -y -qq --no-install-recommends flatpak gir1.2-flatpak-1.0 python3-gi >/dev/null
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
cat > /tmp/teste_flatpak.py <<'EOF'
import os, threading, time
import gi
gi.require_version('Flatpak', '1.0')
from gi.repository import Flatpak, Gio, GLib

inst = Flatpak.Installation.new_user(None)
print('instaladas:', [r.get_name() for r in inst.list_installed_refs_by_kind(Flatpak.RefKind.APP, None)])
print('pasta:', inst.get_path().get_path())

# 1) Só o tamanho: o 'ready' devolve False e a transação pára antes de transferir
tr = Flatpak.Transaction.new_for_installation(inst, None)
tr.set_no_interaction(True)
tr.add_install('flathub', 'app/com.google.Chrome/x86_64/stable', None)
tr.connect('choose-remote-for-ref', lambda *_: 0)
def pronto(t):
    for o in t.get_operations():
        print('  operacao:', o.get_ref(), 'transferir', o.get_download_size() // 1000000, 'MB', 'ocupar', o.get_installed_size() // 1000000, 'MB')
    return False
tr.connect('ready', pronto)
try:
    tr.run(None)
except GLib.Error as e:
    print('parou como esperado:', e.message)

# 2) Progresso real e cancelar ao fim de ~5 MB
canc = Gio.Cancellable()
tr = Flatpak.Transaction.new_for_installation(inst, canc)
tr.set_no_interaction(True)
tr.add_install('flathub', 'app/com.google.Chrome/x86_64/stable', None)
tr.connect('choose-remote-for-ref', lambda *_: 0)
tr.connect('ready', lambda t: True)
eventos = []
def nova(t, op, prog):
    prog.set_update_frequency(300)
    def mudou(p):
        b = p.get_bytes_transferred()
        eventos.append(b)
        if b > 5_000_000 and not canc.is_cancelled():
            print('  progresso:', b // 1000, 'kB,', p.get_progress(), '%, a cancelar')
            canc.cancel()
    prog.connect('changed', mudou)
tr.connect('new-operation', nova)
inicio = time.time()
try:
    tr.run(canc)
    print('terminou sem cancelar?')
except GLib.Error as e:
    print('cancelado:', canc.is_cancelled(), '-', e.message)
print('eventos de progresso:', len(eventos), 'em', round(time.time() - inicio), 's')
EOF
timeout 300 python3 /tmp/teste_flatpak.py
