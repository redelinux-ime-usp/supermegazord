#
# ~/.bash_profile
#

source /etc/profile

# Acrescenta localização dos executáveis pessoais e o diretório corrente ao PATH.

# Acerta algumas variáveis do shell.
#TMOUT=1800
command_oriented_history=t
export command_oriented_history

# Cria arquivo .signature, caso não exista.
if [ ! -f ~/.signature ]; then
  NOME=`finger -m $LOGNAME | grep "Name:" | head -n 1 | cut -d':' -f3`
  echo "$NOME   <$LOGNAME@linux.ime.usp.br>" > .signature
fi

# Inibe a geração de arquivos core.
ulimit -c 0

# Controla a quantidade de ^D consecutivos necessários para se terminar o shell.
export ignoreeof=0

# Executa o ~/.bashrc e o ~/.bash_aliases, se existirem.
if [ -f ~/.bashrc ]; then
  source ~/.bashrc
elif [ -f ~/.bash_aliases ]; then
  source ~/.bash_aliases
fi

# Mostra mensagem idiota. Nao exibe erros se não estiver instalado na máquina.
if [ `which fortune 2> /dev/null | wc -l` -eq 1 ]; then
	echo; fortune; echo
fi

# Checa a cota de disco.
COTA=`quota 2> /dev/null | tail -n 1 | tr -s ' '| cut -d' ' -f2 | egrep "\*$"`
if [ $COTA ]; then
  echo -e '*** Cota de disco estourada! ***\n'
fi

