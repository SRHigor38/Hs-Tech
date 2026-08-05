# 🚀 HS Tech — Site Institucional

Site institucional profissional da **HS Tech**, empresa de tecnologia localizada em **Montes Claros - MG**, especializada em:

- 💻 **Desenvolvimento de Sites**
- 🖥️ **Desenvolvimento de Sistemas**
- ⚡ **Automação de Processos**
- 🔧 **Serviços para Computadores** (montagem, upgrade, formatação, limpeza, suporte técnico)

---

## ✨ Características

| Recurso | Descrição |
|---|---|
| 🎨 Identidade Visual | Dark theme premium, azul `#0A84FF`, neon, glassmorphism, bordas luminosas |
| 📱 Responsivo | Mobile-first, testado de 360px a 1920px |
| ⚡ Performance | CSS/JS modular, fonts self-hosted, zero dependências externas |
| 🔒 Segurança | Validação server-side, escape Jinja2, cookies seguros, headers de segurança |
| ♿ Acessibilidade | WCAG 2.1 AA, navegação por teclado, `prefers-reduced-motion` |
| 🔍 SEO | Meta tags, Open Graph, Schema.org, sitemap.xml |
| ☁️ Deploy | Pronto para GitHub + Render (free tier) |

---

## 🛠️ Tecnologias

- **Python 3.13+**
- **Flask 3.x**
- **Gunicorn** (servidor de produção)
- **HTML5 + CSS3** (design tokens, glassmorphism)
- **JavaScript** (módulos ES6, sem frameworks)

---

## 📁 Estrutura do Projeto

```
HS Tech/
├── app.py                  # Ponto de entrada (dev) + import para Gunicorn (prod)
├── config.py               # Configurações por ambiente (dev/prod/test)
├── requirements.txt        # Dependências Python
├── Procfile                # Comando de inicialização no Render
├── runtime.txt             # Versão do Python no Render
├── render.yaml             # Configuração do deploy no Render
├── .env.example            # Modelo das variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── core/                   # Núcleo da aplicação
│   ├── __init__.py         # Factory: create_app() + security headers
│   ├── extensions.py       # Extensões Flask (futuro: db, login)
│   ├── blueprints/         # Rotas organizadas por módulo
│   ├── services/           # Regras de negócio
│   ├── models/             # (futuro) Entidades do banco
│   └── utils/              # Funções auxiliares
├── templates/              # Templates Jinja2
│   ├── base.html           # Layout mestre
│   ├── partials/           # Componentes reutilizáveis
│   ├── pages/              # Páginas do site
│   └── errors/             # Páginas de erro (404, 500)
└── static/                 # Arquivos estáticos
    ├── css/                # CSS modular (7 arquivos)
    ├── js/                 # JavaScript em módulos ES6
    ├── img/                # Imagens (logo, projetos, OG)
    ├── icons/              # Ícones SVG
    └── fonts/              # Fontes self-hosted
```

---

## 🚀 Como Instalar e Executar Localmente

### 1. Pré-requisitos

- Python 3.11 ou superior
- pip
- Git

### 2. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/hs-tech.git
cd hs-tech
```

### 3. Criar ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar ambiente

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edite o `.env` com os dados da empresa (WhatsApp, e-mail, Instagram).

### 6. Executar

```bash
python app.py
```

Acesse: **http://127.0.0.1:5000**

---

## ☁️ Como Publicar no Render (Grátis)

### Opção A — Blueprint (recomendado)

1. Crie um repositório no GitHub e envie o projeto.
2. Acesse [render.com](https://render.com) e faça login.
3. Clique em **New+ → Blueprint**.
4. Conecte seu repositório GitHub.
5. O Render detectará o arquivo `render.yaml` automaticamente.
6. Clique em **Apply** e aguarde o deploy.

### Opção B — Web Service (manual)

1. Crie um repositório no GitHub e envie o projeto.
2. Acesse [render.com](https://render.com) e faça login.
3. Clique em **New+ → Web Service**.
4. Conecte seu repositório GitHub.
5. Preencha:

| Campo | Valor |
|---|---|
| **Name** | `hs-tech` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | `Free` |

6. Em **Environment**, adicione:

| Variável | Valor |
|---|---|
| `APP_ENV` | `production` |
| `SECRET_KEY` | (gerar forte com: `python -c "import secrets; print(secrets.token_hex(32))"`) |

7. Clique em **Create Web Service** e aguarde.

Seu site estará no ar em: `https://hs-tech.onrender.com`

---

## 🔄 Como Atualizar o Projeto Futuramente

### Localmente

```bash
git pull origin main
pip install -r requirements.txt
python app.py
```

### No Render (automático com Blueprint)

Quando você fizer `git push` no repositório GitHub conectado ao Render, o deploy é feito automaticamente.

---

## 📄 Páginas

| Página | Rota | Descrição |
|---|---|---|
| Home | `/` | Hero, serviços em destaque, diferenciais, projetos |
| Serviços | `/servicos` | As 4 áreas de atuação detalhadas |
| Projetos | `/projetos` | Portfólio com filtro por categoria |
| Sobre | `/sobre` | História, missão, visão e valores |
| Contato | `/contato` | Formulário com validação + WhatsApp |

---

## 🔮 Roadmap Futuro

- [ ] Painel Administrativo
- [ ] Login e autenticação
- [ ] Cadastro de clientes
- [ ] Sistema de orçamentos
- [ ] Dashboard com métricas
- [ ] Banco de dados (SQLAlchemy + Migrations)
- [ ] Blog
- [ ] Área do cliente
- [ ] Integração WhatsApp Business
- [ ] APIs REST
- [ ] Portfólio dinâmico

> A arquitetura do projeto já está preparada para todas essas expansões sem refatoração estrutural.

---

## 🤝 Contato

- **WhatsApp:** [Clique aqui](https://wa.me/5538991388394)
- **E-mail:** hstech.py@gmail.com
- **Instagram:** [@hs.tech.38](https://www.instagram.com/hs.tech.38)
- **Localização:** Montes Claros - MG

---

<div align="center">
  <p>Desenvolvido com 💙 pela <strong>HS Tech</strong></p>
</div>