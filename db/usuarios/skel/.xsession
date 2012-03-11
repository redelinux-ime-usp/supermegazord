#!/bin/sh
# ~/.xsession
# Este é o arquivo pessoal de inicialização do X.

# Abre uma janela para se emitir comandos.
#xterm -sb -sl 500 -j -ls -fn 8x13 -bg black -fg white -geometry 80x25+50+150 -n XTerm -title "`id -un`@`hostname`" &

# Configura o screen saver.
xset s 180 5 s noblank &

echo date >/tmp/data

#Seta as mensagens pra portugues
export LC_ALL=pt_BR

# Carrega o fvwm, que pode ser adaptado a gosto (através do arquivo ~/.fvwmrc).
# exec fvwm -no-m4
# exec fvwm1 -no-m4

# Carrega o kde.
exec gnome-session
