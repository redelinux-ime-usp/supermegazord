# ~/.bash_logout

# Garante que o arquivo .plan exista e tenha, pelo menos, três linhas.
if [ ! -e ~/.plan ]; then
  echo -e "\n\n" > ~/.plan
  LINHAS=3
else
  LINHAS=`wc -l ~/.plan | cut -d'/' -f1`
  if [ $LINHAS -lt 3 ]; then
    echo -e "\n\n" >> ~/.plan
    LINHAS=$[$LINHAS+3]
  fi
fi

# Retira as duas últimas linhas do arquivo .plan e guarda o resultado no
# arquivo /tmp/bash_logout.$$.
head -n $[$LINHAS-2] ~/.plan > /tmp/bash_logout.$$

# Acrescenta duas linhas no final do arquivo /tmp/bash_logout.$$ contendo
# a data e a hora atuais.
date +"Last logout: %a, %d-%h-%Y at %Th" >> /tmp/bash_logout.$$
echo >> /tmp/bash_logout.$$

# Regrava o arquivo .plan com o conteúdo do arquivo /tmp/bash_logout.$$.
mv -f /tmp/bash_logout.$$ ~/.plan > /dev/null

# Limpa a tela da estação antes de fazer o logout.
clear_console -q

# muda de terminal e vai para o gráfico. Isso tem o efeito (desejável) de
# limpar o backbuffer do modo texto para que outros usuários não
# possam bisbilhotar (veja que palavra engraçada)
if tty | grep -q '^/dev/vc/'; then 
   # estamos num terminal modo texto (não num pty do ssh, nem num terminal do X)
   chvt 1
   chvt 7
fi
