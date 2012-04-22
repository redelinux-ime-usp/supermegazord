#!/usr/bin/env python
# -*- coding: utf-8 -*-

# cria_conta: Cria contas da rede a partir de um NID presente no db/users.
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-02

SHELL   = "/bin/bash"

from supermegazord.db import users
from supermegazord.db import path
from supermegazord.lib import cores
from supermegazord.lib import ldapwrap
from supermegazord.lib.account import Account

def wait():
	import getpass
	getpass.getpass("\nPressione ENTER ")

def clear():
	print chr(27) + "[2J"

def wait_and_clear():
	wait()
	clear()

clear()

coletando_nid = True
nid = -1
userinfo = None
while coletando_nid:
	print "Pressione ENTER sem digitar nada para sair.\n"
	nid = raw_input("Preecha o NID do usuário: ").strip()
	if not nid: exit()
	if not users.valida_nid(nid):
		print "Erro: NID inválido."
		wait_and_clear()
		continue

	userinfo = users.get_jupinfo_from_nid(nid)
	if not userinfo:
		print '''O NID que você digitou não está cadastrado no sistema.

  * Se o NID for o número USP de um aluno, então ele não consta como regularmente
    matriculado no IME na última lista do Jupiter obtida da Seção de Alunos.
    Nesse caso, está na hora de ir lá pegar uma atualização!
    %(verm)sNÃO%(norm)s abra a conta do usuário de outra forma!

  * Se você está tentando abrir conta para um não-aluno (e.g. professor)
    você precisa primeiro atribuir-lhe um NID no arquivo db/usuarios/nojup_info''' % cores.allcolors

		wait_and_clear()
		continue
	
	coletando_nid = False

clear()

print "Confirmando dados:"
print
print "NID     : %s" % userinfo.nid
print "Nome    : %s" % userinfo.nome
print "Grupo   : %s" % userinfo.curso
print "Ingresso: %s" % userinfo.ingresso

if users.nid_to_login(nid):
	print "%(verm)sAviso: esse NID já possui conta.%(norm)s" % cores.allcolors, users.nid_to_login(nid) 

wait()

coletando_login = True
login = ""
while coletando_login:
	clear()
	print '''Escolha de login.

Pergunte ao usuario qual login ele deseja ter, respeitando as regras:

1) Pelo menos 2 caracteres e no máximo 12;
2) So pode conter letras minusculas nao acentuadas (a-z);
3) Nao pode ser um nome especial ('root', 'admin', etc).

Aperte ENTER sem digitar nada para cancelar.\n'''
	login = raw_input("Digite o login: ").strip()
	if not login: exit()
	if not users.valida_login(login):
		print "Login inválido."
		wait()
		continue
	
	if login == "root" or login == "admin" or ldapwrap.find_user_by_login(login):
		print "Login indisponível."
		wait()
		continue

	coletando_login = False

home = "/home/" + userinfo.curso + "/" + login
uid  = users.get_next_uid()
gid  = ldapwrap.get_gid(userinfo.curso)

try:
	if int(uid) < 1000:
		print "Recebeu um UID inválido (%s), abortando..." % uid
		exit()
	elif int(gid) < 100:
		print "Recebeu um GID inválido (%s), abortando..." % gid
		exit()
except:
	exit()

newuser = Account(uid, gid, login, userinfo.nome, home, SHELL)
newuser.set_password(users.generate_password())
newuser.set_nid(nid)
newuserdata = {
	'nid': nid,
	'uid': uid,
	'gid': gid,
	'login': login,
	'password': users.generate_password(),
	'curso': userinfo.curso,
	'nome': userinfo.nome,
	'home': home,
	'shell': SHELL }

clear()
print "%(verd)sRESUMINDO:\n" % cores.allcolors
print "NID.....:", newuser.nid
print "Login...:", newuser.login, "(uid = %s)" % newuser.uid
print "Nome....:", newuser.name
print "Grupo...:", userinfo.curso, "(gid = %s)" % newuser.gid
print "Home....:", newuser.home
print "Shell...:", newuser.shell
print cores.norm
print "%(verm)sATENCAO: Ultima chance para desistir.\n" % cores.allcolors
confirm = raw_input("Deseja continuar com a criacao da conta? (y/n) ")
if confirm != "y": exit()

#======================================================
clear()
print "%(verd)sIniciando criação de conta.%(norm)s" % cores.allcolors
print

status_conta = dict()
from supermegazord.lib import kerbwrap
from supermegazord.lib import remote

print "%(azul)s1/8 - Limpando lixo de algum possivel ex-usuario com mesmo login...%(norm)s" % cores.allcolors
# possiveis suspensoes
status_conta['limpeza'] = users.unban_login(newuser.login)

# Adicionando ao passwd (LDAP)
print "%(azul)s2/8 - Adicionando usuário ao passwd (LDAP)...%(norm)s" % cores.allcolors
status_conta['passwd'] = newuser.add_to_ldap()

print "%(azul)s3/8 - Adicionando usuário ao Kerberos...%(norm)s" % cores.allcolors
status_conta['kerberos'] = kerbwrap.add_user(newuser.login, newuser.password) == 0

print "%(azul)s4/8 - Criando home...%(norm)s" % cores.allcolors
# Melhorar ae :)
# tar c -C/opt/megazord-db/usuarios skel | ssh nfs "tar x -C/tmp && chown -R $USER:$GROUP /tmp/skel && mv /tmp/skel /home/$GROUP/$USER && /root/define_quota.sh $USER"
copy_nfs = remote.copy_files("nfs", path.MEGAZORDDB + "usuarios/skel", newuser.home) == 0
if copy_nfs:
	status_conta['home'] = remote.run_script("nfs", "chown -R " + newuser.uid + ":" + newuser.gid + " " + newuser.home) == 0
	remote.run_script("nfs", "/root/define_quota.sh " + newuser.login)
else:
	status_conta['home'] = False

print "%(azul)s5/8 - Criando cota de impressão...%(norm)s" % cores.allcolors
status_conta['print'] = remote.run_script("print", "/root/print/bin/pkadduser " + newuser.login) == 0

print "%(azul)s6/8 - Adicionando usuário nas listas de e-mail...%(norm)s" % cores.allcolors
status_conta['listas'] = remote.run_script("mail", "/root/email/rl_adiciona_pessoa " + userinfo.curso + " " + newuser.login) == 0

print "%(azul)s7/8 - Registrando abertura de conta no histórico do usuário...%(norm)s" % cores.allcolors
msg = "Conta " + newuser.login + (" (%s) aberta\n" % userinfo.curso) + ("NID: %s;" % newuser.nid) + " Nome: %s\n" % newuser.name
status_conta['historico'] = users.add_history_by_nid(newuser.nid, msg)

print "%(azul)s8/8 - Associando NID à conta...%(norm)s" % cores.allcolors
status_conta['nid'] = users.add_nid_login(newuser.nid, newuser.login)

for k in status_conta:
	if status_conta[k]:
		status_conta[k] = cores.verd + " OK " + cores.norm
	else:
		status_conta[k] = cores.verm + "ERRO" + cores.norm

display_login = (newuser.login + "          ")[:12]
display_password = newuser.password

print
print "Operações de cadastro realizadas, exibindo resultados:"
print ".---------------------------------------------------------------------------."
print "| Limpeza   - %(limpeza)s | Passwd    - %(passwd)s | Kerberos  - %(kerberos)s | Home      - %(home)s |" % status_conta
print "| Print     - %(print)s | Listas    - %(listas)s | Historico - %(historico)s | NID       - %(nid)s |" % status_conta
print " --------------------------------------------------------------------------- "
print "|             Login:   " + cores.verd + display_login + cores.norm + "   | Senha:   " + cores.verd + display_password + cores.norm + "                 |"
print " --------------------------------------------------------------------------- "
print
print cores.verm + "                    Devolva a carteirinha do usuário!" + cores.norm
print
wait()
