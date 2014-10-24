#!/bin/bash

EUCLIDES=$(snmpwalk -v 1 -c euclides 192.168.240.41 iso.3.6.1.2.1.43.18.1.1.8 | cut -d'"' -f2)
GALOIS=$(snmpwalk -v 2c -c galois 192.168.240.42 iso.3.6.1.2.1.43.18.1.1.7 | cut -d" " -f4 )
LISTA=rickfg

echo $EUCLIDES > /root/files/tmp/euc1.err
echo $GALOIS > /root/files/tmp/gal1.err

EUC_NEW=$(diff /root/files/tmp/euc.err /root/files/tmp/euc1.err)
GAL_NEW=$(diff /root/files/tmp/euc.err /root/files/tmp/gal1.err)

if [ ["$EUC_NEW" != "" || $GAL_NEW != ""] ]; then
	telnet mail 25 <<EOF
helo linux.ime.usp.br
mail from: $LISTA@linux.ime.usp.br
rcpt to: $LISTA@linux.ime.usp.br
data
Content-Type: text/html; charset=UTF-8
From: Megazord <megazord@linux.ime.usp.br>
To: $LISTA@linux.ime.usp.br
Subject: TESTE: Printer Report
"Euclides: "$EUCLIDES
"GALOIS: "$GALOIS

.

EOF

fi
