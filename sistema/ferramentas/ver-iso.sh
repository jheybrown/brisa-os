#!/bin/bash
# Confirma que a ISO arranca das três formas: BIOS (CD/USB), UEFI, e gravada diretamente numa pen.
# Corre dentro do ambiente Debian de build.
ISO=$(ls /root/obra/brisa-*.iso | head -1)
echo "imagem: $ISO"
echo "--- registos de arranque"
xorriso -indev "$ISO" -report_el_torito plain 2>/dev/null | grep -i "boot img\|MBR\|GPT\|partition" | cut -c1-130
echo "--- pastas de arranque"
xorriso -indev "$ISO" -find /EFI /isolinux /boot/grub -maxdepth 1 2>/dev/null | head -12
echo "--- fundos incluidos"
unsquashfs -l /root/obra/binary/live/filesystem.squashfs 2>/dev/null | grep "usr/share/brisa/fundos/.*[a-z]\.png$" | grep -v mini | sed 's|.*/||' | tr '\n' ' '
echo
