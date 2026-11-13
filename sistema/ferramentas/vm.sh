#!/bin/bash
# Testa a imagem do Brisa numa máquina virtual VirtualBox (corre no Git Bash, no Windows).
#   vm.sh criar <iso>     cria a VM "Brisa-teste" com 2 GB de RAM, como um portátil fraco
#   vm.sh arrancar [gui]  arranca-a (sem janela, ou com janela se "gui")
#   vm.sh captura <png>   guarda uma captura do ecrã da VM
#   vm.sh teclas <...>    envia códigos de teclado (scancodes) à VM
#   vm.sh parar           desliga-a
#   vm.sh apagar          remove a VM e o seu disco
set -e
VB="/c/Program Files/Oracle/VirtualBox/VBoxManage.exe"
VM=Brisa-teste

case "$1" in
  criar)
    iso=$(cygpath -w "$2")
    "$VB" createvm --name "$VM" --ostype Debian_64 --register
    "$VB" modifyvm "$VM" --memory 2048 --cpus 2 --vram 128 --graphicscontroller vmsvga \
      --firmware bios --nic1 nat --audio-enabled off --boot1 dvd --boot2 disk --mouse usbtablet --usb-ohci on --nat-localhostreachable1 on
    pasta=$(dirname "$("$VB" showvminfo "$VM" --machinereadable | sed -n 's/^CfgFile="\(.*\)"$/\1/p' | sed 's/\\\\/\\/g')")
    "$VB" createmedium disk --filename "$pasta\\$VM.vdi" --size 20000
    "$VB" storagectl "$VM" --name SATA --add sata --portcount 2
    "$VB" storageattach "$VM" --storagectl SATA --port 0 --device 0 --type hdd --medium "$pasta\\$VM.vdi"
    "$VB" storageattach "$VM" --storagectl SATA --port 1 --device 0 --type dvddrive --medium "$iso"
    ;;
  arrancar)
    tipo=headless; [ "$2" = gui ] && tipo=gui
    "$VB" startvm "$VM" --type "$tipo"
    ;;
  captura) "$VB" controlvm "$VM" screenshotpng "$(cygpath -w "$2")" ;;
  teclas) shift; "$VB" controlvm "$VM" keyboardputscancode "$@" ;;
  parar) "$VB" controlvm "$VM" poweroff ;;
  apagar) "$VB" unregistervm "$VM" --delete ;;
  *) sed -n '2,9p' "$0" ;;
esac
