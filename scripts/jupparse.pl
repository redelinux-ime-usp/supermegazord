#!/usr/bin/perl
use Getopt::Std;
getopts("o:", \%opts);

$opts{'o'} and do {
   open OUTF, ">$opts{o}" or die "Erro ao gravar $opts{o}.\n$!\n";
   select OUTF;
};

$arq = shift or exec "cat $0 | grep ^\#\# | cut -c4-";

END { unlink("/tmp/jupparse-tmp-$$"); }

# códigos dos cursos:
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
   # 2007-01-04: não existe mais o ciclo básico
   # -- dtiemy
   #/Matem[aá]tica - Ciclo B[aá]sico/ and next; # ignora alunos do ciclo básico
   /^\d/ or next;      # linhas que não começam com número são cabeçalhos

   @f = split /\t+/;
   @f ne 11 and do {
      print STDERR "Aviso: ${linha}: linha mal formatada.\n";
      $falhas++;
      next;
   };

   ($nusp, $nome, $cod, $ingresso, $sufixo) = 
                    ($f[0], $f[2], $f[3], $f[4], $f[7]);

   $cod .= "-$sufixo";

   # Aparentemente (ninguém na seção de alunos soube explicar isso direito)
   # só precisamos olhar para a parte do código de curso que vem antes do
   # hífen. Mas utilizamos a parte que vem depois para decidir entre
   # lic e licn.
   $cod =~ /^(\d+)-(\d+)$/ or do {
      print STDERR "Aviso: ${linha}: código de curso mal formatado: $cod\n";
      $falhas++;
      next;
   };

   $codpref = $1;
   $codsuf = $2;
   
   exists $codcurso{$codpref} or do {
      print STDERR "Aviso: ${linha}: código de curso desconhecido: $cod\n";
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
   # Mudança do formato da data na lista
   # 2006-02-12, dtiemy
   # $ano += ($ano > 40) ? 1900 : 2000;

   printf "${nusp}:${nome}:${grupo}:%04d-%02d-%02d\n", $ano,$mes,$dia;
   $sucessos++;
}

print STDERR "Resumo: $sucessos usuários processados com sucesso\n" .
         "        $falhas linhas da entrada não puderam ser interpretadas\n";

# fóssil da linha principal do script antigo, para referência:
#cat | grep -v -w "Matemática - Ciclo Básico" | \
#perl -ne 'print "$1:$2:$3-$5:$4\n" if (m/(\d+)\s+\d+\s+(\D+\S)\s+(\d+)\s+(\S+).*45\s+(\d+)/);' |  sort -t: -u -n

