#!/bin/bash
# Constrói a imagem ISO do Brisa. Corre como root dentro do WSL (Ubuntu):
#   wsl -d Ubuntu -u root -- bash /mnt/c/.../sistema/construir.sh [limpar]
# Precisa do ambiente Debian 13 em /opt/brisa/trixie (criado com debootstrap).
set -e -o pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
R=/opt/brisa/trixie
OBRA=/root/obra            # pasta de trabalho, vista de dentro do ambiente Debian
SAIDA=/opt/brisa/saida

mkdir -p "$R$OBRA" "$SAIDA"

# A receita vem da pasta do projeto (no Windows); as permissões são repostas aqui
rsync -a --delete --exclude='/.build' --exclude='/cache' --exclude='/chroot' --exclude='/binary' \
  --exclude='/*.iso' --exclude='/*.log' --exclude='/chroot.*' --exclude='/binary.*' --exclude='/brisa-*' \
  "$AQUI/live/auto" "$AQUI/live/config" "$R$OBRA/" 2>/dev/null || \
  { mkdir -p "$R$OBRA"; cp -r "$AQUI/live/auto" "$AQUI/live/config" "$R$OBRA/"; }
find "$R$OBRA/auto" "$R$OBRA/config" -type d -exec chmod 755 {} +
find "$R$OBRA/auto" "$R$OBRA/config" -type f -exec chmod 644 {} +
chmod 755 "$R$OBRA"/auto/* "$R$OBRA"/config/hooks/normal/* "$R$OBRA"/config/includes.chroot/usr/local/bin/*
# Garante finais de linha Unix em tudo o que é texto
find "$R$OBRA/auto" "$R$OBRA/config" -type f -exec sed -i 's/\r$//' {} +

cat > "$R/root/lb-construir.sh" <<'EOF'
#!/bin/bash
set -e
cd /root/obra
if [ "$1" = limpar ]; then lb clean --purge; else lb clean; fi
lb config
lb build
EOF
chmod 755 "$R/root/lb-construir.sh"

# Se a construção falhar, o script pára aqui e a imagem anterior em $SAIDA fica intacta
if ! bash "$AQUI/ferramentas/entrar.sh" bash /root/lb-construir.sh "$1" 2>&1 | tee "$SAIDA/construir.log"; then
  echo "ERRO: a construcao falhou; ver $SAIDA/construir.log" >&2
  exit 1
fi

ISO=$(ls "$R$OBRA"/brisa-*.iso 2>/dev/null | head -1)
if [ -n "$ISO" ]; then
  cp "$ISO" "$SAIDA/brisa.iso"
  ls -lh "$SAIDA/brisa.iso"
else
  echo "ERRO: a imagem nao foi criada; ver $SAIDA/construir.log" >&2
  exit 1
fi
