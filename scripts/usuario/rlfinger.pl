#!/usr/bin/perl
#
## Script do MEGAZORD
##___________________________________________________________________________
## -> Nome: rlfinger
## -> DescriÃ§Ã£o: Mostra todas as informaÃ§Ãµes do usuÃ¡rio <info>, onde <info> pode ser
## o NID dele, o login dele, parte do nome ou o nome completo (no caso do nome completo, passe-o
## para o script entre aspas duplas. Ex: rlfinger "Arnaldo Mandel".
## -> Uso: rlfinger <info>
## -> Por: Alberto Bueno Junior (Login: abueno)
## -> Ultima Atualizacao: 26/03/2010
##____________________________________________________________________________

use utf8;
binmode(STDOUT, ":utf8");

# Caminho dos scripts e tudo mais
$megazord = "/root/supermegazord/";
# require "/root/megazord/backends/include";

if (!@ARGV) { # Se nao tem argumentos, mostra uma interface:
	print "${verm}ERRO: ${amar}Nenhum argumento foi passado. Fechando!${norm}\n";
	exit 0;
}

$info = $ARGV[0];
chomp $info;
$opcao = $ARGV[1];
chomp $opcao;

# Checa o tipo de entrada
$tipo_de_info = "";
if ($info =~ /^[0-9]+$/) {
	$tipo_de_info = "nid";	
}
if ($info =~ /^[a-z]+$/) {
	$tipo_de_info = "login";
}
if ($info =~ /^([A-Z])([a-z]+)(\s)([A-Z])([a-z]+)/) {
	$tipo_de_info = "nome_completo";
}
if ($info =~ /^([A-Z])([a-z]+)$/) {
	$tipo_de_info = "nome_incompleto";
}

# Dado a entrada, encontra o NID
if ($tipo_de_info eq "nid") {
	chomp $info;
	$login = qx(loginfor $info);
	chomp $login;
	if ($login eq "") {
		print "${verm}ERRO: Usuario ${amar}$info ${verm}nao encontrado. Fechando!\n${norm}";
		exit 0;
		
	}
	$nid = $info;
}
if ($tipo_de_info eq "login") {
	$nid = qx(nidfor $info);
	if ($nid eq "") {
		print "${verm}ERRO: Usuario ${amar}$info ${verm}nao encontrado. Fechando!\n${norm}";
		exit 0;
	}
	chomp $nid;
}
if ($tipo_de_info eq "nome_completo") {
	$nid = qx(nidfor `ypcat passwd | grep -w \"$info\" | cut -d":" -f1`);
	if ($nid eq "") {
		print "${verm}ERRO: Usuario ${amar}$info ${verm}nao encontrado. Fechando!\n${norm}";
		exit 0;
	}
	chomp $nid;
}
if ($tipo_de_info eq "nome_incompleto") {
	@nids = qx(ypcat passwd | grep \"$info\" | cut -d":" -f1);
	foreach (@nids) {
		chomp $_;
		system "rlfinger $_";
	}
	exit 0;
}
if ($nid eq "") { # Se nao caiu em nenhum dos casos acima, fecha
	print "${verm}ERRO: Entrada nao reconhecida. Fechando!${norm}\n";
	exit 0;
	
}

# Agora que sabemos o NID (e que ele é válido!), vamos tirar todas as informações do usuário

$login = qx(loginfor $nid); chomp $login;
$pwline = qx(ypcat passwd | grep ^$login:); chomp $pwline;
$pwline =~ /^$login:.*?:(\d+):(\d+):(.*?):(.*?):/
	or die "ERRO: linha do passwd incorretamente formatada:\n$pwline\n";
($uid, $gid, $nome_completo, $home) = ($1, $2, $3, $4);
$grupo = qx(groupfor $gid); chomp $grupo;
$ingresso = qx(cat ${backends}/usuarios/jup_info | grep ^$nid: | cut -d":" -f4); chomp $ingresso;
if ($ingresso eq "") {
	$ingresso = "${amar}Usuario consta apenas no nojup_info";
}
$n_emails_novos = qx(ls -1 /home/$grupo/$login/Maildir/new | wc -l); chomp $n_emails_novos;

$suspenso = qx(cat ${backends}/usuarios/suspensoes | grep ^$login:);
if ($suspenso eq "") {
	$suspenso = 0;
}
else {
	$suspenso = 1;
	$suspensao_data = qx(cat ${backends}/usuarios/suspensoes | grep ^$login: | cut -d":" -f2); chomp $suspensao_data;
	$suspensao_motivo = qx(cat ${backends}/usuarios/suspensoes | grep ^$login: | cut -d":" -f3); chomp $suspensao_motivo;
}

$ex_admin = qx(cat ${backends}/usuarios/ex_admins | grep ^$nid:);
if ($ex_admin eq "") {
	$ex_admin = 0;
}
else {
	$ex_admin = 1;
}

$admin = qx(cat ${backends}/usuarios/admins | grep $login);
if ($admin eq "") {
	$admin = 0;
}
else {
	$admin = 1;
}

if ($opcao eq "-c") { # Pesquisa completa
	$n_torrents_found = qx(find /home/$grupo/$login -name "*".torrent | wc -l); chomp $n_torrents_found;
}
else {
	$n_torrents_found = 0;
}

$foto = "/home/bcc/abueno/$login.jpg";
#$foto = "${backends}/tmp/$login.jpg";
#$foto = "/tmp/$login.jpg";
#system "ssh thewho \"wget --progress=bar -O $foto \\\"http://sistemas2.usp.br/jupiterweb/exibirFotoPessoa?codpes=6514202&status=D\\\" \"";
#system "scp thewho:$foto /home/bcc/abueno/Desktop/";


#system "clear";
print "${cian}===========================================================================\n";
print "${azul}| Nome    : ${verd}$nome_completo\n";
print "${azul}| NID     : ${verd}$nid\n";
print "${azul}| Login   : ${verd}$login\n";
print "${azul}| UID     : ${verd}$uid\n";
print "${azul}| Grupo   : ${verd}$grupo\n";
print "${azul}| GID     : ${verd}$gid\n";
print "${azul}| Home    : ${verd}$home\n";
print "${azul}| Ingresso: ${verd}$ingresso\n";
print "${azul}| E-mails : ${verd}$n_emails_novos\n";
if ($suspenso == 1) {
	print "${azul}----------------------------------------------------------\n";
	print "${azul}| ${verm}O usuario esta suspenso desde ${amar}$suspensao_data${verm}. Motivo: ${amar}$suspensao_motivo\n";
}
if ($ex_admin == 1) { 
	print "${azul}----------------------------------------------------------\n";
	print "${azul}| ${amar}* Ex-Admin!\n";
}
if ($admin == 1) {
	print "${azul}----------------------------------------------------------\n";
	print "${azul}| ${amar}* ${verd}Admin!\n";
#	system "rangers &";
}
if ($n_torrents_found != 0) {
	print "${azul}----------------------------------------------------------\n";
	print "${azul}| ${amar}* ${verm}$n_torrents_found ${amar}\".torrent\"'s encontrados na conta do usuario!\n";
}
print "${azul}----------------------------------------------------------${verd}\n";
system "${backends}/scripts/quota $login";
print "${azul}----------------------------------------------------------${verd}\n";
system "${backends}/scripts/quotap $login";
print "${azul}----------------------------------------------------------${verd}\n";
print "${azul}Historico do usuario:${verd}\n";
system "cat ${backends}/usuarios/historicos/$nid";
print "${cian}===========================================================================\n\n\n\n";

#system "rm -f $foto";
#system "zgv $foto";
