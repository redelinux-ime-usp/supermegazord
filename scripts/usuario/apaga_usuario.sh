#/bin/bash

if [ $# -ne 1 ]; then
	echo "Uso: $0 <usuário>"
	exit 1
	fi

DEL=$1

# ... mktemp
LDIF=$(mktemp)
echo "dn: uid=$DEL,ou=People,dc=linux,dc=ime,dc=usp,dc=br" >> $LDIF
echo "changetype: modify" >> $LDIF
echo "delete: userPassword" >> $LDIF
ldapmodify -D cn=admin,dc=linux,dc=ime,dc=usp,dc=br -y /opt/megazord-db/secrets/ldap -f $LDIF

kadmin -p megazord/admin -q "delprinc $DEL" -w $(cat /opt/megazord-db/secrets/kerberos)

ssh megazord@nfs sudo /megazord/apaga_usuario.sh $DEL

# TODO: e-mail eterno, tirar das listas

echo "Conta '$DEL' encerrada." >> /opt/megazord-db/log/encerrado
