# HS Tech

Site institucional Flask para desenvolvimento de software, com portfólio, formulário de orçamento e painel administrativo. Os serviços são apresentados na Home. O item Contato abre o WhatsApp configurado; Orçamento abre o formulário interno.

## Execução local

1. Instale Python 3.11 ou superior e crie um ambiente virtual: `python -m venv .venv`.
2. Ative o ambiente e instale `pip install -r requirements.txt`.
3. Copie `.env.example` para `.env` e configure uma chave secreta e banco SQLite **novo** para desenvolvimento. Não envie `.env` ou bancos ao controle de versão.
4. Para banco vazio: `python -m flask --app app db upgrade`. Em banco existente, faça backup e verifique o histórico antes de aplicar migrações; não aplique a migração inicial diretamente sobre tabelas preexistentes.
5. Crie um administrador somente quando não existir outro: `python -m flask --app app create-admin`. A senha é pedida sem eco.
6. Execute `python app.py` e abra o endereço local informado. O painel é `/admin/login`.

Execute os testes com `python -m unittest discover -s tests -v`. Os testes usam bancos de memória, não o banco de desenvolvimento.

## Recursos e documentos

O painel permite administrar solicitações, projetos, serviços, galeria e configurações da marca. A política de privacidade fica em `/privacidade`. Projetos em rascunho não são públicos. As demonstrações são independentes e exclusivamente locais; seus caminhos e limitações constam em [DEMONSTRACOES.md](DEMONSTRACOES.md).

Consulte [MANUAL_ADMIN.md](MANUAL_ADMIN.md), [PRODUCAO.md](PRODUCAO.md) e [ACOMPANHAMENTO.md](ACOMPANHAMENTO.md). A plataforma ainda requer revisão e testes de infraestrutura antes da publicação. Não há deploy automático autorizado por esta documentação.

## Preparação para Render

O modelo `render.yaml` e o [GUIA_RENDER.md](GUIA_RENDER.md) descrevem uma configuração futura. Ainda faltam testes com PostgreSQL e Redis reais, imagens revisadas para os três rascunhos, backups operacionais e validação de HTTPS. Não sincronize ou faça deploy sem autorização.

O portfólio está sendo preparado para apresentar os projetos demonstrativos por imagens explicativas; as aplicações interativas não serão disponibilizadas no lançamento. A Barbearia está publicada no banco local; imagens e publicação local do Personal Trainer e da loja permanecem pendentes: veja [PORTFOLIO_IMAGENS.md](PORTFOLIO_IMAGENS.md).
