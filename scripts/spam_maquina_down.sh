#!/bin/bash

DOWN=$(/opt/bin/watchman --down clients)
LISTA=batata

if [ "$DOWN" != "" -a 1 == 2 ]; then
	telnet mail 25 <<EOF
helo linux.ime.usp.br
mail from: $LISTA@linux.ime.usp.br
rcpt to: $LISTA@linux.ime.usp.br
data
Content-Type: text/html; charset=UTF-8
From: Megazord <megazord@linux.ime.usp.br>
To: $LISTA@linux.ime.usp.br
Subject: Máquinas Desligadas
$DOWN

.

EOF

fi
