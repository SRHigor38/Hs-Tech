# 📚 Documentação Técnica — HS Tech

## 1. Arquitetura

O projeto segue o padrão **MVC (Model-View-Controller)** com **camada de serviços**:

```
┌─────────────────────────────────────────────────────────┐
│                    USUÁRIO (Browser)                     │
└──────────────────────────┬──────────────────────────────┘
                           │ HTTP Request
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    FLASK / Gunicorn                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Blueprints  │  │   Services   │  │   Models      │  │
│  │ (Rotas)      │  │ (Negócio)    │  │ (Futuro)      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬────────┘  │
│         │                 │                 │           │
│         ▼                 ▼                 ▼           │
│  ┌───────────────────────────────────────────────┐      │
│  │              Jinja2 (Templates)                │      │
│  └───────────────────────┬───────────────────────┘      │
│                          ▼                               │
│              HTML + CSS + JS (estáticos)                 │
└──────────────────────────┼──────────────────────────────┘
                           ▼
                  Resposta HTML
```

### Padrões utilizados

| Padrão | Aplicação |
|---|---|
| **Application Factory** | `create_app()` em `core/__init__.py` |
| **Blueprints** | Rotas por módulo (main, servicos, projetos) |
| **Camada de Services** | Regras de negócio isoladas em `core/services/` |
| **Config por ambiente** | `config.py` com classes dev/prod/test |
| **Security Headers** | Aplicados via `after_request` em todas as respostas |
| **Context Processors** | Dados globais (empresa, ano, WhatsApp) injetados nos templates |

---

## 2. Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.13+ | Linguagem principal |
| Flask | 3.0.3 | Framework web |
| Gunicorn | 23.0.0 | Servidor WSGI de produção |
| Jinja2 | (via Flask) | Template engine |
| HTML5 | — | Estrutura das páginas |
| CSS3 | — | Design tokens, glassmorphism, responsividade |
| JavaScript | ES6 | Módulos: menu, animações, formulário |
| python-decouple | 3.8 | Variáveis de ambiente |
| python-dotenv | 1.0.1 | Carregamento do .env |

---

## 3. Funcionalidades

### Páginas

| Página | Rota | Funcionalidades |
|---|---|---|
| **Home** | `/` | Hero, serviços em destaque, diferenciais, projetos recentes, CTA |
| **Serviços** | `/servicos` | 4 áreas detalhadas com cards e âncoras |
| **Projetos** | `/projetos` | Portfólio com filtro por categoria (JS) |
| **Sobre** | `/sobre` | História, missão, visão, valores, diferenciais |
| **Contato** | `/contato` | Formulário validado + envio via WhatsApp |

### Funcionalidades transversais

- Botão flutuante do WhatsApp em todas as páginas
- Menu mobile (hamburger) com animação
- Scroll reveal com IntersectionObserver
- Formulário com validação em tempo real e máscara de telefone
- Páginas de erro 404 e 500 personalizadas
- SEO: meta tags, Open Graph, Twitter Cards, Schema.org JSON-LD
- Sitemap.xml e robots.txt
- Favicon SVG da marca
- Fontes self-hosted (Sora + Inter)

---

## 4. Estrutura das Pastas

```
HS Tech/
├── app.py                  # Entry point (dev) + import Gunicorn (prod)
├── config.py               # Configurações por ambiente
├── requirements.txt        # Dependências
├── Procfile                # Comando de inicialização (Render)
├── runtime.txt             # Versão do Python (Render)
├── render.yaml             # Blueprint de deploy (Render)
├── .env.example            # Modelo de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── README.md               # Guia de instalação e deploy
├── DOCUMENTACAO.md         # Este documento
│
├── core/                   # Núcleo da aplicação
│   ├── __init__.py         # Factory + security headers + error handlers
│   ├── extensions.py       # Extensões Flask (futuro)
│   ├── blueprints/         # Rotas por módulo
│   │   ├── __init__.py     # Registro central
│   │   ├── main_routes.py  # Home, Sobre, Contato
│   │   ├── servicos_routes.py
│   │   └── projetos_routes.py
│   ├── services/           # Regras de negócio
│   │   └── content_service.py
│   ├── models/             # (futuro) Entidades do banco
│   └── utils/              # Helpers e validators
│
├── templates/              # Jinja2
│   ├── base.html           # Layout mestre
│   ├── partials/           # Navbar, footer, cards, CTA, WhatsApp
│   ├── pages/              # 5 páginas
│   └── errors/             # 404, 500
│
└── static/                 # Arquivos estáticos
    ├── css/                # 7 módulos CSS
    ├── js/                 # 4 módulos JS
    ├── img/                # Logo, projetos, OG
    ├── icons/              # Favicon
    └── fonts/              # Sora + Inter
```

---

## 5. Fluxo do Sistema

### Fluxo de uma requisição

1. Usuário acessa `/servicos`
2. Gunicorn (produção) ou Flask (dev) recebe a requisição
3. O Blueprint `servicos` chama a view `servicos()`
4. A view chama `get_servicos()` da camada de services
5. O service retorna os dados (hoje estáticos, futuramente do banco)
6. O Flask renderiza `templates/pages/servicos.html` com os dados
7. O Jinja2 injeta os dados no HTML e envia a resposta
8. O CSS estiliza e o JS adiciona interatividade

### Fluxo do formulário de contato

1. Usuário preenche o formulário
2. JS valida em tempo real (nome, e-mail, telefone, assunto, mensagem)
3. Ao enviar, o JS monta a mensagem formatada
4. Abre o WhatsApp com `https://wa.me/5538991388394?text=...`
5. Mostra feedback de sucesso e limpa o formulário

---

## 6. Possíveis Melhorias Futuras

### Banco de dados
- Ativar SQLAlchemy + Flask-Migrate
- Modelos: Cliente, Projeto, Servico, Orcamento, Mensagem, Usuario
- Migrations versionadas

### Painel Administrativo
- Login com Flask-Login
- CRUD de projetos, serviços e mensagens
- Dashboard com métricas

### Área do Cliente
- Acompanhamento de orçamentos
- Sistema de chamados/suporte
- Agendamento de serviços

### Integrações
- WhatsApp Business API
- Envio de e-mails
- Pagamentos (PIX, cartão)
- APIs REST próprias

### Performance
- Minificação de CSS/JS em produção
- Cache de estáticos
- Lazy loading de imagens
- CDN para assets

### SEO
- Blog com categorias e tags
- URLs amigáveis com slugs
- Sitemap dinâmico

---

## 7. Segurança Implementada

| Proteção | Implementação |
|---|---|
| **XSS** | Escape automático do Jinja2 (`{{ }}`) |
| **SQL Injection** | ORM parametrizado (futuro) |
| **CSRF** | Token CSRF (futuro com Flask-WTF) |
| **Headers de segurança** | `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` |
| **Cookies seguros** | `HttpOnly`, `SameSite=Lax`, `Secure` em produção |
| **Secret Key** | Obrigatória em produção via variável de ambiente |
| **Validação server-side** | `core/utils/validators.py` |
| **Debug desativado** | `DEBUG=False` em produção |

---

<div align="center">
  <p>Documentação da <strong>HS Tech</strong> — 2026</p>
</div>