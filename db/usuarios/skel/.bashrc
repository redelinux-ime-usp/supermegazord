#!/bin/bash
# ~/.bashrc
source /etc/profile

# Ativa o bash_completion, se estiver instalado
if [ -f /etc/bash_completion ]; then
	source /etc/bash_completion
fi

# Executa o ~/.bash_aliases, se existir
if [ -f ~/.bash_aliases ]; then
	source ~/.bash_aliases
fi

# Configura a aparência do prompt do shell
export PS1='[\h:\w]\$ '

# Adiciona o diretório bin do usuário ao PATH
export PATH="~/bin:$PATH"

# Configura o idioma
export LC_ALL="pt_BR.UTF-8"
export LANG="pt_BR.UTF-8"

# Checa a quota de disco
QUOTA=`quota 2> /dev/null | tail -n 1 | tr -s ' '| cut -d' ' -f2 | egrep "\*$"`
if [ $QUOTA ]; then
	echo -e '\n*** Cota de disco estourada! - Apague seus arquivos ou contate um admin ***\n'
fi
