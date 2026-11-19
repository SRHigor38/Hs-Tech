# Relatório de desenvolvimento local — 18/11/2026

## Implementado nesta continuação

- Configurações administrativas com autenticação, CSRF, validação e imagens verificadas; integração com informações públicas e WhatsApp.
- Página de privacidade e proteção de cache para páginas sensíveis; requisitos mínimos de configuração de produção para segredo, banco e limitador compartilhado.
- Dependências Flask, Pillow e python-dotenv atualizadas após auditoria e teste. Correções de depreciações e fechamento de banco nos testes.
- Comando de backup SQLite para destino novo, com verificação de integridade e teste de recuperação em arquivo descartável.
- README, manual do painel, guia de instalação, guia de produção e checklist revisados.

## Arquivos principais

`core/blueprints/configuracoes.py`, `core/blueprints/main_routes.py`, `core/blueprints/solicitacoes.py`, `core/blueprints/__init__.py`, `core/utils/helpers.py`, `core/models.py`, `core/forms.py`, `core/extensions.py`, `config.py`, `requirements.txt`, `.env.example`, `render.yaml`; templates públicos e administrativos de navegação, configurações, privacidade e textos; `scripts/backup_sqlite.py`; testes de configurações, produção e backup; documentos README.md, MANUAL_ADMIN.md, GUIA_INSTALACAO.md, PRODUCAO.md, CHECKLIST_PUBLICACAO.md, ACOMPANHAMENTO.md e DEMONSTRACOES.md. O projeto já possuía outras alterações locais anteriores, preservadas.

## Migrações e banco

Nenhuma migração nova foi necessária. As migrações existentes e `db check` passaram em banco vazio e em cópia descartável do banco de desenvolvimento. Nenhuma migração foi aplicada ao banco existente nesta continuação.

## Testes e limites

15 testes da aplicação passaram no ambiente virtual com dependências atualizadas. Testes locais das três demonstrações passaram. `pip check` não identificou conflitos e `pip-audit` não encontrou vulnerabilidades conhecidas no ambiente verificado; resultados são pontuais. As páginas públicas e telas administrativas indicadas no acompanhamento foram medidas em 375/768/1280/1920 px, sem rolagem horizontal nas medições; não foi feita auditoria completa de acessibilidade/contraste. Foram testados backup e restauração de SQLite descartável. Redis real, múltiplos processos, PostgreSQL, proxy HTTPS, persistência e monitoramento em infraestrutura ainda não foram testados.

## Pendências e riscos

Definir retenção e revisar privacidade/LGPD; testar rate limit com Redis e processos reais; testar banco e servidor escolhidos para produção; implementar armazenamento persistente, logs com rotação, monitoramento, alertas e backup de arquivos; revisar ativos, referências externas, dados e segurança das três demos; isolar a rede na infraestrutura; revisar autenticação, recuperação e configuração de implantação. As demonstrações continuam locais e os registros em rascunho. Nenhuma segurança de produção é garantida pelos testes locais.

## Início local e publicação

Siga README.md e GUIA_INSTALACAO.md para criar ambiente, instalar dependências, migrar apenas banco novo e criar administrador quando necessário. Consulte PRODUCAO.md e CHECKLIST_PUBLICACAO.md antes de uma publicação. A publicação ou qualquer mudança de infraestrutura externa depende de autorização explícita.


## Continuação — testes e preparação complementar

Foram adicionados logs JSON mínimos, com rotação opcional em arquivo para processo único, e testes que verificam que dados fictícios de senha não aparecem nos eventos. O padrão stderr é o recomendado para coleta coordenada entre múltiplos processos. Os logs de servidores e proxies exigem tratamento separado.

Os scripts de backup do banco e dos uploads foram testados em dados descartáveis; a restauração de uploads exige diretório novo e rejeita travessia de diretórios e links simbólicos. O backup conjunto não é atômico; a operação precisa coordenar gravações ou usar snapshots de infraestrutura. Criada proposta não executada em RETENCAO_DADOS.md.

Sem Redis local, Docker ou WSL, foi executado teste alternativo de duas aplicações compartilhando um servidor fakeredis em loopback. Uma instalação com configuração de produção descartável usou SQLite em disco, servidor Waitress local, upload fictício persistente e cookies Secure/HttpOnly. O resultado não comprova Redis real, TLS, Gunicorn ou infraestrutura de produção.

Nas demos, exemplos numéricos de telefone foram substituídos por máscaras e o Personal deixou de aceitar metadados externos no cadastro de exercícios; os testes das três demos passaram. Uma busca por padrões não constitui revisão integral nem prova ausência de dados sensíveis.

Incluído atalho de teclado para conteúdo, corrigida navegação do menu móvel e ajustado contraste dos botões principais; Tab, Enter e Escape foram exercitados no navegador. Não houve auditoria completa de leitor de tela ou contraste de todos os elementos. A suíte principal atual passou com 19 testes, incluindo falha da página de erro, e a auditoria pip-audit do ambiente isolado não encontrou vulnerabilidades conhecidas.

**Situação:** o site principal ainda não está tecnicamente pronto para publicação. Pendentes: Redis real compartilhado, HTTPS e proxy, persistência e backups consistentes no ambiente escolhido, logs de servidores/proxies, alertas e testes de recuperação, definição de retenção e revisão de privacidade, revisão de acessibilidade e auditoria de segurança. As demos permanecem rascunhos locais e requerem auditoria e isolamento de infraestrutura antes de qualquer exposição. Nenhum deploy foi realizado.


## Atualização: remoção do simulador

O simulador citado em etapas históricas foi retirado da aplicação e da Home. A rota `/simulador` retorna 404, e os arquivos exclusivos de interface e recomendação foram removidos. A suíte atual contém 17 testes aprovados em banco isolado. Os bancos existentes não foram alterados e nenhum deploy foi realizado.
