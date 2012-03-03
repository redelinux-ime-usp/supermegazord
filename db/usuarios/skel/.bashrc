#
# ~/.bashrc
#

source /etc/profile

# Verifica se o shell é interativo.
if [ "$PS1" ]; then

  # Executa o ~/.bash_aliases, se existir.
  if [ -f ~/.bash_aliases ]; then
    source ~/.bash_aliases
  fi

  # Configura a aparência do prompt do shell
  PS1='[\h:\w]\$ '
  PS2='> '
  export PS1 PS2

  export PATH="$PATH:."
fi

