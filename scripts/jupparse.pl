#!/usr/bin/perl
#
## Script do MEGAZORD
##___________________________________________________________________________
## -> Nome: jupparse
## -> Descri��o: Script que faz o parsing da lista do j�piter trazido da se��o
## de alunos, gerando o arquivo "jup_info".
## -> Uso: jupparse [-o arquivo_saida] <arquivo-secao-alunos>
## -> Por: Alberto Bueno Junior (Login: abueno)
## -> Ultima Atualizacao: 26/03/2010
##____________________________________________________________________________

# Caminho dos scripts e tudo mais
$backends = "/root/megazord/backends";

require "/root/megazord/backends/include";

use Getopt::Std;
getopts("o:", \%opts);

$opts{'o'} and do {
   open OUTF, ">$opts{o}" or die "Erro ao gravar $opts{o}.\n$!\n";
   select OUTF;
};

$arq = shift or exec "cat $0 | grep ^\#\# | cut -c4-";

END { unlink("/tmp/jupparse-tmp-$$"); }

# c�digos dos cursos:
%codcurso = (
             "45010" => "bm",
             "45021" => "lic",
             "45022" => "lic",
             "45023" => "lic",
             "45024" => "lic",    
             "45031" => "bm",
             "45040" => "bma",
             "45041" => "bmac",
             "45042" => "bma",
             "45050" => "bcc",
             "45051" => "bcc",
             "45060" => "be",
             "45061" => "be",
             "45070" => "bmac",
); 

open FILE, $arq or die "Erro ao abrir $arq\n$!\n";
$linha = 0;
$sucessos = 0;
$falhas = 0;
while (<FILE>) {
   $linha++;
   chomp;
   # 2007-01-04: n�o existe mais o ciclo b�sico
   # -- dtiemy
   #/Matem[a�]tica - Ciclo B[a�]sico/ and next; # ignora alunos do ciclo b�sico
   /^\d/ or next;      # linhas que n�o come�am com n�mero s�o cabe�alhos

   @f = split /\t+/;
   @f ne 11 and do {
      print STDERR "Aviso: ${linha}: linha mal formatada.\n";
      $falhas++;
      next;
   };

   ($nusp, $nome, $cod, $ingresso, $sufixo) = 
                    ($f[0], $f[2], $f[3], $f[4], $f[7]);

   $cod .= "-$sufixo";

   # Aparentemente (ningu�m na se��o de alunos soube explicar isso direito)
   # s� precisamos olhar para a parte do c�digo de curso que vem antes do
   # h�fen. Mas utilizamos a parte que vem depois para decidir entre
   # lic e licn.
   $cod =~ /^(\d+)-(\d+)$/ or do {
      print STDERR "Aviso: ${linha}: c�digo de curso mal formatado: $cod\n";
      $falhas++;
      next;
   };

   $codpref = $1;
   $codsuf = $2;
   
   exists $codcurso{$codpref} or do {
      print STDERR "Aviso: ${linha}: c�digo de curso desconhecido: $cod\n";
      $falhas++;
      next;
   };

   $grupo = $codcurso{$codpref};
   $grupo = "licn" if $grupo eq 'lic' && $codsuf =~ /^4/;

   $ingresso =~ /^(\d\d?)\/(\d\d?)\/((\d\d)?\d\d)/ or do {
      print STDERR "Aviso: ${linha}: data de ingresso mal formatada\n";
      $falhas++;
      next;
   };

   ($dia, $mes, $ano) = ($1, $2, $3);
   # Mudan�a do formato da data na lista
   # 2006-02-12, dtiemy
   # $ano += ($ano > 40) ? 1900 : 2000;

   printf "${nusp}:${nome}:${grupo}:%04d-%02d-%02d\n", $ano,$mes,$dia;
   $sucessos++;
}

print STDERR "Resumo: $sucessos usu�rios processados com sucesso\n" .
         "        $falhas linhas da entrada n�o puderam ser interpretadas\n";

# f�ssil da linha principal do script antigo, para refer�ncia:
#cat | grep -v -w "Matem�tica - Ciclo B�sico" | \
#perl -ne 'print "$1:$2:$3-$5:$4\n" if (m/(\d+)\s+\d+\s+(\D+\S)\s+(\d+)\s+(\S+).*45\s+(\d+)/);' |  sort -t: -u -n

