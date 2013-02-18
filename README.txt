Dependencias:
 - python2.7

Configurações:
 - Pasta onde esse README.txt se encontra precisa estar no PATH do python.
 - DNS configurado.
 - MEGAZORD_DB no script supermegazord.db.path configurado

MEGAZORD_DB:
	secrets/
 		keys/			- Cada arquivo $M nesse diretório é uma chave privada de SSH que loga em $M, com o usuário 'megazord'. Essa chave não deve possuir senha.
		ldap			- Senha para o usuário cn=admin,dc=linux,dc=ime,dc=usp,dc=br do LDAP.
		kerberos		- Senha para o principal "root/admin" do Kerberos.
	maquinas/
		grupos.conf		- Arquivo que define os grupos de máquinas do módulo supermegazord.db.machines. Verifique a documentação do módulo para maiores informações.
	usuarios/
		skel/			- Esqueleto da home criada para usuários novos. Certifique-se que as permissões estão corretas, pois estas são copiadas.
		jupiter/
			jup_info	- Arquivo gerado apartir dos dados coletados mais recentes. Não altere.
			nojup_info	- Entradas especiais vão aqui.

Outros servidores:

Necessita de um usuário 'megazord' em: nfs, mail, printer
Tal usuário deve ser um sudoer capaz de executar os seguintes scripts, sem senha:

nfs:
	/megazord/cria_conta.sh

mail:
	/root/email/rl_adiciona_pessoa

printer:
	/root/files/bin/pkadduser


--- FERRAMENTAS DO MEGAZORD

CLI:

-> supermegazord users
 Ferramentas para manipular as 
