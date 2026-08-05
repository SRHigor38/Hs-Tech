"""
HS Tech — Serviço de Conteúdo.

Camada de regras de negócio responsável por fornecer os dados de conteúdo
do site (serviços, projetos, diferenciais, missão/visão/valores).

ATENÇÃO: Hoje os dados são estáticos (estruturas Python).
Futuramente, serão consultados no banco de dados via SQLAlchemy.
As rotas e templates NÃO precisarão ser alterados,
pois o formato de retorno será mantido.

Exemplo futuro:
    def get_servicos():
        return Servico.query.filter_by(ativo=True).order_by(Servico.ordem).all()
"""


def get_servicos() -> list[dict]:
    """
    Retorna todas as áreas de serviço da empresa com seus sub-serviços.

    Returns:
        list[dict]: Lista de áreas de serviço.
    """
    return [
        {
            "id": "sites",
            "slug": "sites",
            "titulo": "Desenvolvimento de Sites",
            "subtitulo": "Sites modernos, rápidos e que vendem",
            "icone": "code",
            "descricao": (
                "Criamos sites institucionais, landing pages e lojas virtuais "
                "com design premium, performance otimizada e foco em conversão. "
                "Seu negócio merece uma presença digital profissional."
            ),
            "itens": [
                "Sites institucionais",
                "Landing pages de alta conversão",
                "Lojas virtuais (e-commerce)",
                "Sites totalmente responsivos",
                "Otimização para mecanismos de busca (SEO)",
                "Manutenção e atualizações",
            ],
            "cor": "#0A84FF",
            "destaque": True,
        },
        {
            "id": "sistemas",
            "slug": "sistemas",
            "titulo": "Desenvolvimento de Sistemas",
            "subtitulo": "Soluções web sob medida para seu negócio",
            "icone": "cpu",
            "descricao": (
                "Desenvolvemos sistemas web personalizados para automatizar, "
                "organizar e otimizar a gestão da sua empresa. Do planejamento "
                "à entrega, criamos a solução ideal para o seu processo."
            ),
            "itens": [
                "Sistemas web personalizados",
                "Sistemas de gestão interna",
                "Dashboards e relatórios gerenciais",
                "Integração com APIs",
                "Sistemas para controle de estoque",
                "Sistemas para controle financeiro",
            ],
            "cor": "#38B6FF",
            "destaque": True,
        },
        {
            "id": "automacoes",
            "slug": "automacoes",
            "titulo": "Automação de Processos",
            "subtitulo": "Tecnologia que trabalha por você",
            "icone": "zap",
            "descricao": (
                "Eliminamos tarefas repetitivas e manuais com automações "
                "inteligentes. Seus processos rodando sozinhos, com mais "
                "velocidade, precisão e produtividade."
            ),
            "itens": [
                "Automação de tarefas e processos",
                "Bots para atendimento e rotinas",
                "Geração automática de relatórios",
                "Integrações entre sistemas",
                "Web scraping e coleta de dados",
                "Notificações e alertas automáticos",
            ],
            "cor": "#6DC5FF",
            "destaque": True,
        },
        {
            "id": "computadores",
            "slug": "computadores",
            "titulo": "Serviços para Computadores",
            "subtitulo": "Seu computador rápido, seguro e funcionando",
            "icone": "monitor",
            "descricao": (
                "Serviços completos para desktops e notebooks: montagem, "
                "upgrade, formatação, limpeza e suporte técnico especializado. "
                "Devolvemos performance e confiabilidade ao seu equipamento."
            ),
            "itens": [
                "Montagem de computadores",
                "Upgrade de hardware (SSD, RAM, placa de vídeo)",
                "Formatação e instalação de Windows",
                "Limpeza e manutenção preventiva",
                "Instalação de programas",
                "Remoção de vírus e otimização",
                "Suporte técnico presencial e remoto",
            ],
            "cor": "#0A84FF",
            "destaque": True,
        },
    ]


def get_servicos_destaque() -> list[dict]:
    """Retorna os serviços exibidos na Home (todos são destaque)."""
    return get_servicos()


def get_projetos() -> list[dict]:
    """
    Retorna todos os projetos do portfólio.

    Futuro: consulta ao banco de dados (modelo Projeto).
    """
    return [
        {
            "id": 1,
            "titulo": "Site Institucional — Construtora Alfa",
            "categoria": "Sites",
            "descricao": "Site completo com design premium, galeria de obras e integração com WhatsApp.",
            "imagem": "img/projetos/projeto-site-construtora.svg",
            "tecnologias": ["Flask", "JavaScript", "CSS"],
            "destaque": True,
        },
        {
            "id": 2,
            "titulo": "Sistema de Gestão — Distribuidora Beta",
            "categoria": "Sistemas",
            "descricao": "Sistema web para controle de estoque, pedidos e emissão de relatórios gerenciais.",
            "imagem": "img/projetos/projeto-sistema-gestao.svg",
            "tecnologias": ["Flask", "SQLAlchemy", "Bootstrap"],
            "destaque": True,
        },
        {
            "id": 3,
            "titulo": "Automação de Relatórios — Financeira Gama",
            "categoria": "Automações",
            "descricao": "Bot que gera relatórios financeiros diários automaticamente e envia por e-mail.",
            "imagem": "img/projetos/projeto-automacao-relatorios.svg",
            "tecnologias": ["Python", "APIs", "Scheduler"],
            "destaque": True,
        },
        {
            "id": 4,
            "titulo": "Landing Page — Clínica Delta",
            "categoria": "Sites",
            "descricao": "Landing page de alta conversão com agendamento online integrado.",
            "imagem": "img/projetos/projeto-landing-clinica.svg",
            "tecnologias": ["HTML", "CSS", "JavaScript"],
            "destaque": False,
        },
        {
            "id": 5,
            "titulo": "E-commerce — Loja Épsilon",
            "categoria": "Sites",
            "descricao": "Loja virtual completa com carrinho, pagamentos e painel de pedidos.",
            "imagem": "img/projetos/projeto-ecommerce.svg",
            "tecnologias": ["Flask", "JavaScript", "APIs"],
            "destaque": False,
        },
        {
            "id": 6,
            "titulo": "Upgrade de Hardware — Escritório Zeta",
            "categoria": "Computadores",
            "descricao": "Upgrade de 15 máquinas com SSD e memória RAM, mais que dobrando a performance.",
            "imagem": "img/projetos/projeto-upgrade-hardware.svg",
            "tecnologias": ["Hardware", "Otimização"],
            "destaque": False,
        },
    ]


def get_projetos_destaque() -> list[dict]:
    """Retorna os projetos em destaque para a Home (máximo 3)."""
    projetos = get_projetos()
    destaques = [p for p in projetos if p["destaque"]]
    return destaques[:3]


def get_diferenciais() -> list[dict]:
    """Retorna os diferenciais da empresa."""
    return [
        {
            "titulo": "Atendimento Personalizado",
            "descricao": (
                "Cada projeto é único. Ouvimos suas necessidades e entregamos "
                "uma solução sob medida para o seu objetivo."
            ),
            "icone": "chat",
        },
        {
            "titulo": "Prazo e Qualidade",
            "descricao": (
                "Compromisso com prazos combinados e qualidade impecável "
                "em cada entrega. Seu tempo é valioso."
            ),
            "icone": "clock",
        },
        {
            "titulo": "Suporte Contínuo",
            "descricao": (
                "Não sumimos após a entrega. Oferecemos suporte contínuo "
                "para garantir que tudo continue funcionando perfeitamente."
            ),
            "icone": "shield",
        },
        {
            "titulo": "Tecnologia de Ponta",
            "descricao": (
                "Utilizamos as melhores tecnologias e práticas de mercado "
                "para entregar soluções modernas, rápidas e seguras."
            ),
            "icone": "rocket",
        },
    ]


def get_missao_visao_valores() -> list[dict]:
    """Retorna Missão, Visão e Valores da empresa."""
    return [
        {
            "titulo": "Nossa Missão",
            "descricao": (
                "Transformar ideias em soluções tecnológicas que geram "
                "resultados reais para nossos clientes, com qualidade, "
                "inovação e atendimento humano."
            ),
            "icone": "target",
        },
        {
            "titulo": "Nossa Visão",
            "descricao": (
                "Ser referência em desenvolvimento de sites, sistemas e "
                "serviços de tecnologia, reconhecida pela excelência e "
                "confiança entregue em cada projeto."
            ),
            "icone": "eye",
        },
        {
            "titulo": "Nossos Valores",
            "descricao": (
                "Compromisso, transparência, inovação, qualidade e respeito "
                "ao cliente. São esses pilares que guiam cada decisão "
                "e cada entrega da HS Tech."
            ),
            "icone": "heart",
        },
    ]