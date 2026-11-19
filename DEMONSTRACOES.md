# Preparação das demonstrações

## Estado atual

As cópias técnicas de trabalho foram criadas no espaço de trabalho do Codex. Elas ainda não são demonstrações prontas e não devem ser expostas. Bancos, arquivos `.env`, credenciais de arquivo, imagens, uploads, arquivos compactados e caches foram excluídos da cópia. Código e templates ainda podem conter nomes, contatos, dados de exemplo ou configurações sensíveis e precisam de revisão antes da execução ou compartilhamento. Os originais permanecem intactos.

## Barbearia HF

O projeto usa Flask, SQLAlchemy, Flask-WTF e Flask-Bcrypt. Foram identificados modelos para clientes, profissionais, serviços, agendamentos, planos, despesas e registros financeiros. Há autenticação administrativa própria e fluxos de plano e agendamento. Os arquivos incluem referências a links de WhatsApp e os modelos registram dados pessoais e financeiros. A inicialização do projeto original também cria dados iniciais e pode criar um administrador de desenvolvimento, portanto não deve ser usada com o banco original nem com credenciais padrão em um ambiente público.

Antes de integrar: revisar todos os templates, dados de inicialização e assets; substituir a marca e contatos; bloquear mensagens e operações externas; usar banco novo exclusivo com dados fictícios; definir conta e permissões demonstrativas restritas; testar restauração ou isolamento de alterações. Registros financeiros não devem produzir cobranças reais.

## Personal Trainer

O aplicativo real está dentro da subpasta `personal_trainer` e usa Flask, SQLAlchemy, Flask-Login, Flask-WTF e Flask-Migrate. Foram identificados modelos de usuários, alunos, exercícios, fichas e sessões, com rotas para profissional e aluno. Os modelos podem conter telefone, data de nascimento, observações e histórico de treino. Há integração de busca de exercícios com wger, inclusive referências a URLs de mídia externa.

Antes de integrar: usar banco novo independente e migrado; criar apenas contas e dados fictícios; revisar dados embutidos no código e templates; desligar ou simular wger e mídia externa; restringir dados e operações; testar restauração ou isolamento de alterações.

## Exposição

Não há links públicos para essas cópias. Antes de disponibilizar, é necessário comprovar que não acessam os bancos originais nem a rede externa, revisar a autenticação, definir a política de reset e executar testes funcionais e de segurança. Para produção, planejar processos, bancos e armazenamento separados por demonstração.

Revisão complementar das cópias técnicas: a cópia da Barbearia contém referências externas, endereços de e-mail e links de WhatsApp em arquivos de código ou templates; a cópia do Personal Trainer contém referências externas e uma rotina de dados de aluno pré-definidos. São necessários revisão e remoção ou substituição segura antes da inicialização como demonstração. Contagens apenas indicam padrões no código e não comprovam que os dados sejam reais; nenhum conteúdo foi publicado. Próxima ação: inventariar e neutralizar essas referências, configurar bancos novos e bloquear rede de saída, depois testar com dados fictícios.

## Barbearia — protótipo local isolado

Foi preparada uma versão derivada da cópia técnica em `work/demos-isoladas/barbearia-demo`. O iniciador `demo_local.py` fixa o servidor em 127.0.0.1:5110, cria banco SQLite em memória e sessão com cookie próprio, bloqueia conexões de saída via sockets da aplicação e rejeita requisições com origem fora de loopback. Links de WhatsApp, referências externas de interface e a identidade anterior foram removidos dos arquivos de execução; uploads estão desativados. O acesso de demonstração à gestão é intencionalmente local e sem credenciais compartilhadas; dados, nomes e valores são ilustrativos. Reiniciar o processo cria banco vazio com serviços e profissional fictícios. A versão atual cria uma instância e um banco em memória separados por sessão de visitante.

Teste `python teste_demo_local.py`: verificados banco em memória, bloqueio de IP não local e conexão externa, CSRF, bloqueio de upload, agendamento fictício, conflito e visualização na gestão. Um novo processo confirmou banco sem agendamentos. Formulário inspecionado no navegador em 375 px. Não há garantia de ausência de todo dado sensível no código; apenas padrões e caminhos inspecionados foram revisados. O bloqueio implementado não equivale a isolamento de rede do sistema operacional. A cópia é somente local, não está integrada à HS Tech e não deve ser exposta publicamente sem revisão adicional, isolamento por visitante, testes de segurança e bloqueio de saída em nível de infraestrutura.


## Atualização: isolamento local por visitante

As cópias executáveis locais em `work/demos-isoladas/barbearia-demo` e `work/demos-isoladas/personal-trainer-demo` usam, cada uma, um gerenciador em processo único que cria instância Flask, chave de sessão e SQLite em memória independentes para cada sessão. O identificador do visitante é aleatório; o cookie expira em 30 minutos e instâncias inativas são removidas após 30 minutos quando chegam novas requisições. O limite atual é 12 sessões locais por demonstração. Ao reiniciar, todos os bancos temporários são descartados. Isso não é um serviço multiprocessos ou uma solução de isolamento de infraestrutura.

A Barbearia usa a porta local 5110 e o Personal Trainer 5111. O último inclui profissional, aluno, exercício e ficha fictícios; sua entrada demonstra os papéis de profissional e aluno. O endpoint de busca wger e uploads estão bloqueados. Em ambas as cópias, requisições de fora de loopback e cabeçalhos Host não locais são recusados, conexões de saída por sockets Python são bloqueadas e há uma política CSP restritiva. Esses mecanismos não substituem firewall e isolamento do sistema operacional.

Testes locais: duas sessões simultâneas, bancos separados, tentativa de reutilização do cookie de autenticação, expiração, restauração, CSRF, agendamento e gestão da Barbearia; no Personal, criação de aluno fictício, acesso às fichas e início de sessão, papéis e bloqueio wger. Dois visitantes HTTP simultâneos em cada porta receberam identificadores diferentes. Revisão por padrões nos arquivos executáveis não encontrou os contatos e nomes específicos antes identificados, mas não comprova ausência de todos os dados sensíveis. Imagens e outros assets excluídos das cópias ainda precisam ser revisados ou substituídos. Não há links públicos nem garantias de segurança para publicação.

Foram criados dois registros em rascunho no banco de desenvolvimento da HS Tech, sem imagens e sem URLs de demonstração; acesso público aos dois retornou 404. Para publicar futuramente: revisar todos os arquivos e assets, testar continuamente fluxo e segurança, definir isolamento por visitante e reset na infraestrutura real, bloquear rede de saída em nível de sistema e usar processos e armazenamento separados.


## E-commerce — demonstração exclusivamente local (18/11/2026)

Criada em `C:/Users/higor/Documents/Codex/2026-11-18/files-pasted-by-the-user-projeto/work/demos-isoladas/ecommerce-demo`, independente da HS Tech e das demais demonstrações. `python demo_local.py` inicia em `127.0.0.1:5112`; requer Flask e Flask-WTF. Catálogo, categorias, busca, produto, carrinho, pedido e confirmação são fictícios; a gestão demonstra produtos, categorias, estoque e status de pedidos. Não coleta contato ou cartão e não realiza pagamentos, entregas, mensagens ou integrações externas. O cancelamento recompõe o estoque fictício uma única vez; reabrir o pedido verifica e reserva novamente as quantidades disponíveis.

Cada visitante recebe Flask e SQLite em memória próprios, com chave e cookie próprios; gestão acessível por botão apenas para aquela sessão local, com CSRF. Limite de 12 sessões por processo, cookie de 30 minutos, expiração após 30 minutos de inatividade na próxima requisição e restauração pelo reinício. Rejeita Host e endereço não locais e uploads; CSP limita recursos e o iniciador bloqueia sockets de saída. Esses controles são locais e **não substituem isolamento de rede de infraestrutura**, nem servem como autenticação para publicação. Não disponibilizar externamente.

Testes `python test_loja.py`: 4 testes passaram, cobrindo busca, filtro, carrinho, quantidades, pedido, estoque, cadastro/edição, categorias, status e reposição de estoque no cancelamento, dois visitantes simultâneos, isolamento, CSRF, autorização, expiração, restauração, upload, Host/IP e bloqueio de socket do iniciador. Servidor local retornou HTTP 200. Interface inspecionada no navegador em 375 e 1280 px; sem rolagem horizontal na largura móvel medida. Essas verificações não constituem auditoria de segurança nem teste de infraestrutura.

Registro `demonstracao-ecommerce` criado no banco de desenvolvimento como rascunho, sem imagem e URL; Barbearia, Personal Trainer e loja permanecem rascunhos e retornaram 404 ao público. Backup antes da inclusão em `instance/backup_antes_ecommerce_20261118_120410.db`. Imagens reais de apresentação e infraestrutura segura permanecem pendentes.


## Nova verificação local — 18/11/2026

Os testes existentes da Barbearia, Personal Trainer e loja passaram novamente, incluindo cenários locais de isolamento, CSRF e expiração descritos acima. A busca por referências a conexões externas, pagamentos, WhatsApp e wger identificou arquivos adicionais nas cópias derivadas da Barbearia e Personal Trainer. Isso exige revisão antes de qualquer disponibilização; a busca por padrões não demonstra ausência integral de dados pessoais ou integrações. O bloqueio em sockets e a separação em processo único não substituem firewall, autenticação e isolamento real de infraestrutura. Não foram alterados projetos originais nem criadas URLs públicas.

Inventário adicional por padrões: 53 arquivos Python/HTML/CSS/JS na Barbearia, 53 no Personal e 11 na loja. Nenhum endereço HTTP textual foi detectado nos arquivos examinados da Barbearia ou loja; no Personal foram identificadas referências a wger.de, Creative Commons e ao namespace W3C. A rota de busca wger continua bloqueada na aplicação local e a política CSP restringe imagens externas, mas arquivos de serviço e interface ainda contêm referências que exigem revisão. Uma busca textual não inspeciona semanticamente todos os dados ou prova segurança. Um arquivo de backup de JavaScript de um byte também foi identificado na cópia do Personal; não foram detectados endereços ou números longos nele.


## Revisão complementar de segurança local

A busca de padrões em código, templates e assets identificou exemplos numéricos de telefone em cinco arquivos da cópia da Barbearia; foram substituídos por máscaras sem números, preservando os originais. Na cópia do Personal, o formulário de exercícios agora apresenta cadastro manual sem busca externa; metadados e URLs externas enviados manualmente são ignorados pelo servidor, e a rota wger continua bloqueada. O código legado da integração permanece na cópia, inativo nesse fluxo. Testes locais das três demonstrações passaram após as alterações, incluindo tentativa de enviar metadados wger pelo formulário.

A inspeção por padrões encontrou zero arquivos com e-mails ou credenciais literais correspondentes aos padrões utilizados nas três cópias após a revisão; isso não substitui leitura e auditoria integral nem prova ausência de dados sensíveis, referências externas indiretas ou vulnerabilidades. As três demos continuam locais, não são segurança de produção e não devem ser expostas antes de isolamento de infraestrutura e revisão independente.
