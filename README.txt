Dependencias (pacotes do debian wheezy)
 - python2.7
 - python-ldap
 - python-paramiko
 - krb5-user

Configurações:
 - Um arquivo supermegazord.pth dentro do site-packages cujo conteúdo é um diretório acima
    do diretório onde esse README.txt se encontra.
 - DNS configurado.
 - MEGAZORD_DB no script supermegazord.db.path configurado

MEGAZORD_DB:
    conf/
        ldap.conf       - Define o BASEDN, a URI e o ROOTDN do servidor ldap.
    secrets/
        keys/           - Cada arquivo $M nesse diretório é uma chave privada de SSH que loga em 
                           $M, com o usuário 'megazord'. Essa chave não deve possuir senha.
        ldap            - Senha para o ROOTDN do LDAP.
        kerberos        - Senha para o principal "root/admin" do Kerberos.
    maquinas/
        grupos.conf     - Define os grupos de máquinas do módulo supermegazord.db.machines.
                           Verifique a documentação do módulo para maiores informações.
    usuarios/
        skel/           - Esqueleto da home criada para usuários novos. Certifique-se que as 
                          permissões estão corretas, pois estas são copiadas.
        historicos/     - Diretório onde se encontra o histórico de cada conta. Escrito 
                           automaticamente por account.log
        jupiter/
            jup_info    - Arquivo gerado apartir dos dados coletados mais recentes. Não altere.
            nojup_info  - Entradas especiais vão aqui.

Outros servidores:

Necessita de um usuário 'megazord' em: nfs, mail, printer
Tais servidores devem ter tal entrada no sudoers:
megazord    ALL=(root) NOPASSWD: /megazord/scripts/*

--- FERRAMENTAS DO MEGAZORD

CLI:

Utilize o argumento -h (ou --help) para maiores detalhes de algum comando específico.

-> supermegazord accounts
 Ferramentas para manipular as contas de usuários do sistema. Possui os seguintes comandos:

 => search
   Busca e imprime na tela informações de contas, com suporte a filtros.

 => deactivate/reactivate
   Desativa e ativa contas. Método de encerrar contas de ex-alunos.

 => newpassword
   Gera uma nova senha aleatória para a conta do usuário.

-> supermegazord machines
 Lista as máquinas da rede. Possui opções para listar ips e/ou macs e filtrar por salas.

-> supermegazord precadastro
 Gerencia o precadastro de contas.

 => lista
   Lista todos os pré-cadastros existentes do momento.
 => status
   Determina se um NID ou login está disponível, está pré-cadastrado ou já utilizado.
 
 => adiciona
   Realiza um pré-cadastro manualmente, sem necessidade de utilizar o formulário web. Internamente,
   o formulário web utiliza esse comando.
 
 => remove
   Apaga um pré-cadastro, sem efetivá-lo.
 
 => finaliza
   Finaliza o pré-cadastro, criando uma conta com os dados deste. Isso remove o pré-cadastro
   automaticamente.
   Em caso de erro, verifique o histórico do NID para maiores detalhes.

-> supermegazord watchman
 Visualiza o estado das máquinas da rede. Pode ser utilizado com argumentos para imprimir valores 
 úteis para scripts, como máquinas desligadas ou ligadas, com opção de filtrar por sala(s).

