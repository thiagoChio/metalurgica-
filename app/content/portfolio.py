"""Portfolio, depoimentos e FAQ.

IMPORTANTE
----------
Nenhum projeto, depoimento ou numero aqui e real. Todos sao PLACEHOLDERS
estruturais, marcados com `is_placeholder = True`, para que o layout possa ser
montado e testado antes de existir material fotografico.

O site NAO exibe estatisticas nem depoimentos enquanto forem placeholders --
ver `app/content/__init__.py`. Preencha com material real e mude a flag.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    category: str
    location: str
    summary: str
    materials: tuple
    purpose: str
    images: tuple = ()
    cover_image: str = ""
    is_placeholder: bool = True

    @property
    def cover(self) -> str:
        """Capa do card (corte 4:3). Sem foto, cai no desenho técnico."""
        if self.cover_image:
            return self.cover_image
        if self.images:
            return self.images[0]
        return f"/media/blueprint/{self.slug}.svg"

    @property
    def gallery(self) -> tuple:
        return self.images if self.images else (self.cover,)


PROJECTS: tuple = (
    Project(
        slug="cobertura-area-gourmet",
        title="Cobertura em policarbonato",
        category="Coberturas",
        location="Cuiabá/MT",
        summary="Estrutura metálica com telha de policarbonato sobre área gourmet.",
        materials=("Estrutura em metalon", "Telha de policarbonato", "Pintura eletrostática"),
        purpose="Cobrir a área de convívio sem escurecer o ambiente: o policarbonato "
                "protege da chuva e deixa passar a luz natural.",
        images=("/static/img/projetos/cobertura-policarbonato-g.webp",),
        cover_image="/static/img/projetos/cobertura-policarbonato.webp",
        is_placeholder=False,
    ),
    Project(
        slug="cobertura-patio",
        title="Cobertura de pátio",
        category="Coberturas",
        location="Cuiabá/MT",
        summary="Cobertura de grande vão com treliça e telha trapezoidal.",
        materials=("Treliça metálica", "Telha trapezoidal", "Colunas tubulares"),
        purpose="Vencer o vão do pátio inteiro com poucas colunas, liberando a área "
                "de baixo para circulação e manobra.",
        images=("/static/img/projetos/cobertura-patio-g.webp",
                "/static/img/projetos/cobertura-patio-interna-g.webp"),
        cover_image="/static/img/projetos/cobertura-patio.webp",
        is_placeholder=False,
    ),
    Project(
        slug="portao-fabricacao",
        title="Portão em fabricação",
        category="Portões e grades",
        location="Oficina — Cuiabá/MT",
        summary="Quadro montado, barras posicionadas e solda em execução.",
        materials=("Tubo quadrado", "Barra chata", "Solda MIG"),
        purpose="A montagem é feita sobre gabarito, com as barras alinhadas antes de "
                "soldar — é o que garante o portão sem empeno depois de instalado.",
        images=("/static/img/projetos/portao-fabricacao-g.webp",),
        cover_image="/static/img/projetos/portao-fabricacao.webp",
        is_placeholder=False,
    ),
    Project(
        slug="estrutura-fachada",
        title="Estrutura para fachada",
        category="Fachadas e letreiros",
        location="Cuiabá/MT",
        summary="Estrutura metálica de sustentação para painel de fachada comercial.",
        materials=("Perfil tubular", "Chumbadores", "Tratamento anticorrosivo"),
        purpose="Sustentar o painel da fachada com ancoragem dimensionada para vento — "
                "a parte que ninguém vê é a que segura o letreiro no lugar.",
        images=("/static/img/projetos/estrutura-fachada-g.webp",),
        cover_image="/static/img/projetos/estrutura-fachada.webp",
        is_placeholder=False,
    ),
)


@dataclass(frozen=True)
class Testimonial:
    name: str
    city: str
    project_type: str
    text: str
    is_placeholder: bool = True


TESTIMONIALS: tuple = (
    Testimonial("[NOME DO CLIENTE]", "[CIDADE]", "[TIPO DE PROJETO]", "[DEPOIMENTO REAL DO CLIENTE]"),
    Testimonial("[NOME DO CLIENTE]", "[CIDADE]", "[TIPO DE PROJETO]", "[DEPOIMENTO REAL DO CLIENTE]"),
    Testimonial("[NOME DO CLIENTE]", "[CIDADE]", "[TIPO DE PROJETO]", "[DEPOIMENTO REAL DO CLIENTE]"),
)


@dataclass(frozen=True)
class Stat:
    value: str
    label: str
    is_placeholder: bool = True


# NUNCA publicar numeros inventados. Preencher com dados reais e is_placeholder=False.
STATS: tuple = (
    Stat("[ANOS]", "Anos de atuação"),
    Stat("[QTD]", "Projetos entregues"),
    Stat("[QTD]", "Clientes atendidos"),
)


@dataclass(frozen=True)
class FaqItem:
    question: str
    answer: str
    needs_review: bool = False


FAQ: tuple = (
    FaqItem(
        "Vocês fazem sob medida?",
        "Sim — é a regra da casa. Praticamente tudo parte de medida tirada no local. "
        "Tem projeto ou croqui? Trabalhamos em cima dele. Não tem? A gente desenvolve junto.",
    ),
    FaqItem(
        "Como funciona o orçamento?",
        "Você manda pelo WhatsApp o que precisa, com foto do local se tiver. Retornamos "
        "para entender os detalhes e, quando necessário, agendamos a medição. "
        "Só então enviamos a proposta com material, prazo e valor.",
    ),
    FaqItem(
        "Quais cidades vocês atendem?",
        "Cuiabá, Várzea Grande e região. A oficina fica na Av. Canadá, no Santa Rosa. "
        "Para obras fora dessa área, consulte — dependendo do porte da estrutura compensa.",
    ),
    FaqItem(
        "Posso mandar foto e medida pelo WhatsApp?",
        "Pode, e é o jeito mais rápido. Com foto do local e a medida aproximada, "
        "o primeiro retorno já sai com uma ideia de solução.",
    ),
    FaqItem(
        "Qual é o prazo?",
        "Depende do porte da peça, do material e da agenda da produção. "
        "O prazo vai junto com a proposta, antes de qualquer compromisso.",
    ),
    FaqItem(
        "Vocês fazem estrutura para fachada e letreiro?",
        "Fazemos. É a estrutura que sustenta o painel — dimensionada para o peso "
        "e para o vento, com ancoragem adequada e tratamento anticorrosivo.",
    ),
    # ---------------------------------------------------------------- pendentes
    # As três abaixo NÃO aparecem no site enquanto needs_review=True.
    # Confirme a resposta com a empresa e troque a flag para publicar.
    FaqItem(
        "O orçamento tem custo?",
        "[CONFIRMAR: o orçamento é gratuito? A visita para medição é cobrada?]",
        needs_review=True,
    ),
    FaqItem(
        "A instalação está inclusa?",
        "[CONFIRMAR: instalação inclusa no valor ou cobrada à parte? Há limite de distância?]",
        needs_review=True,
    ),
    FaqItem(
        "Quais as formas de pagamento?",
        "[CONFIRMAR: formas aceitas, percentual de sinal e parcelamento.]",
        needs_review=True,
    ),
)
