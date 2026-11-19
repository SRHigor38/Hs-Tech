# Preparação para produção — ainda não publicada

Estas orientações não autorizam publicação, contratação ou alteração de infraestrutura. Todas as configurações devem ser revistas e testadas no ambiente real antes de qualquer deploy autorizado.

## Ambiente e dados

- Configure `APP_ENV=production`, `SECRET_KEY` aleatória com ao menos 32 caracteres e `DATABASE_URL` persistente. A aplicação exige `RATELIMIT_STORAGE_URI` Redis (`redis://` ou `rediss://`) compartilhado entre processos. Defina limites de rede e autenticação adequados para o Redis; não exponha o serviço publicamente. O funcionamento com uma instância Redis real ainda precisa ser testado.
- Use banco persistente, backups e migrações revisadas. SQLite deve ficar em disco persistente; avalie limites de concorrência e um banco de servidor para maior carga. A compatibilidade com PostgreSQL e seu driver ainda não foi validada.
- O comando `gunicorn app:app` é destinado a Linux; configure workers, timeouts, reinício de processo e proxy reverso no ambiente final. Gunicorn não é servidor Windows nativo. Coloque HTTPS no proxy, use certificados válidos e cookies Secure; confie em cabeçalhos encaminhados apenas quando os proxies confiáveis forem definidos e testados.
- Monte `static/img/projetos/uploads` em armazenamento persistente com permissões restritas de gravação. Inclua imagens e banco nos backups; revise o acesso público aos uploads antes da publicação. Arquivos desvinculados não são apagados automaticamente.

## Backup e restauração

Para SQLite, com Python instalado, `python scripts/backup_sqlite.py CAMINHO_DO_BANCO CAMINHO_NOVO_DO_BACKUP` cria uma cópia consistente e verifica integridade. O destino deve ser novo; nunca sobrescreve um arquivo. Copie também o diretório de uploads e guarde as cópias cifradas, com acesso restrito e política de retenção definida.

Teste restauração offline: pare a aplicação de teste, copie o backup para um **novo caminho**, verifique `PRAGMA integrity_check`, restaure os uploads em uma pasta isolada e inicie uma instância de teste apontando para a cópia. Nunca sobrescreva o banco de produção sem plano de recuperação aprovado. Os backups contêm dados pessoais e precisam de proteção e descarte adequado.

## Operação e verificação

Configure logs com rotação, sem senhas, tokens ou conteúdo dos formulários, e monitoramento de disponibilidade, erros, uso de disco, banco, Redis, certificados e sucesso dos backups. Verifique autenticação, mudança de senha inicial, CSRF, uploads, links, integridade das migrações, recuperação em caso de falhas e rate limiting entre processos. Defina prazo de retenção, tratamento dos pedidos de titulares, responsáveis e revisão jurídica da política de privacidade.

Antes de publicar: revisar vulnerabilidades das versões instaladas, instalação limpa, TLS, dependências, variáveis, `DEBUG=False`, segredo forte, serviços persistentes, permissões, teste de backup/restore, observabilidade, proteção de dados e restrição de acesso administrativo. Revise as demonstrações separadamente: processos descartáveis isolados, autenticação e controles de recursos, rede de saída bloqueada no nível de infraestrutura, expiração e limpeza reais. Isolamento em um processo Python não é suficiente. Manter todos os projetos demonstrativos em rascunho até avaliação e autorização.


## Continuação: logs, cópias e verificação isolada

O aplicativo emite eventos JSON com horário, nível, tipo e, nas requisições, método, nome interno da rota e status. Não registra URL, query, IP, parâmetros, formulários, cabeçalhos nem conteúdo de exceções. Por padrão envia os eventos para stderr; para rotação local em um único processo defina `HS_LOG_DIR` para diretório persistente e protegido. A rotação interna mantém até cinco arquivos anteriores de 10 MB. `RotatingFileHandler` não coordena múltiplos processos: em múltiplos workers, use stderr e um coletor que faça rotação de forma segura. Logs do servidor WSGI, proxy ou plataforma são separados e devem ser configurados para não incluir URLs, query strings, IPs ou dados sensíveis; os controles do aplicativo não os higienizam. A ausência de mensagens e tracebacks nos logs do aplicativo limita a investigação; planeje diagnóstico restrito sem expor dados.

`python scripts/backup_uploads.py backup DIRETORIO_UPLOADS ARQUIVO_NOVO.zip` cria arquivo novo; `python scripts/backup_uploads.py restore ARQUIVO.zip DIRETORIO_NOVO` restaura em pasta nova sem sobrescrever. Não aceita links simbólicos ou caminhos que escapem do destino e impõe limites de tamanho e quantidade. Verifique integridade, permissões e completude após restauração. Os dois passos não são uma captura atômica conjunta do banco e dos uploads; para um backup consistente entre eles, interrompa gravações ou use snapshot coordenado da infraestrutura. No erro, restos parciais são preservados para análise.

Teste opcional descartável: instale `requirements-test.txt` em ambiente isolado e execute `python scripts/verificar_producao_local.py`. O script usa fakeredis (simulação), SQLite descartável, servidor Waitress preso a loopback e upload em pasta temporária; verifica limite compartilhado por dois processos e atributos de cookie. Não testa um Redis real, Gunicorn, HTTPS, rede externa nem o servidor final. O Redis e a infraestrutura reais devem ser validados antes da publicação.

Consulte [RETENCAO_DADOS.md](RETENCAO_DADOS.md) para a proposta ainda não aprovada de retenção.

## Preparação para Render

Consulte [GUIA_RENDER.md](GUIA_RENDER.md) para o roteiro, variáveis e custos. `render.yaml` é um modelo local com web `0.5c-512mb`, uma instância e disco de 1 GB para uploads; sincronizar um Blueprint pode criar e publicar recursos, e exige autorização. Driver psycopg 3 incluído; SQL de migrações foi gerado offline, mas conexão e migrações em PostgreSQL real ainda não foram comprovadas. Os ajustes de proxy e de IP só devem ser habilitados atrás da borda Render e testados contra falsificação. PostgreSQL, Redis e backups reais permanecem pendentes.
