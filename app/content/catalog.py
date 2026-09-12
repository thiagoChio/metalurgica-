"""Catalogo de servicos e diferenciais.

Editar este arquivo altera o site inteiro sem tocar em HTML ou CSS.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Service:
    slug: str
    number: str
    title: str
    summary: str
    detail: str
    applications: tuple
    materials: tuple
    whatsapp_subject: str

    @property
    def anchor(self) -> str:
        return f"servico-{self.slug}"


SERVICES: tuple = (
    Service(
        slug="estruturas",
        number="01",
        title="Estruturas Metálicas",
        summary="Dimensionadas para o vão e a carga da sua obra.",
        detail=(
            "Fabricamos estruturas em aço para obras residenciais, comerciais e industriais. "
            "O dimensionamento parte do vão a ser vencido, da carga prevista e da forma de "
            "fixação disponível no local, para que a estrutura trabalhe dentro do que foi projetado."
        ),
        applications=("Galpoes", "Lajes e entrepisos", "Reforços estruturais", "Bases e apoios"),
        materials=("Perfil I e H", "Tubo retangular", "Cantoneira", "Chapa dobrada"),
        whatsapp_subject="uma estrutura metálica",
    ),
    Service(
        slug="portoes",
        number="02",
        title="Portões",
        summary="Basculante, deslizante ou pivotante — sob medida.",
        detail=(
            "O portão é a primeira coisa que se vê em um imóvel e a que mais sofre com uso diário. "
            "Fabricamos considerando peso, tipo de acionamento, desnível do terreno e o espaço "
            "disponível para abertura, para que o portão continue funcionando bem anos depois."
        ),
        applications=("Residencial", "Condominio", "Comercial", "Industrial"),
        materials=("Chapa lisa e perfurada", "Tubo galvanizado", "Aluminio", "Ripado metálico"),
        whatsapp_subject="um portão",
    ),
    Service(
        slug="coberturas",
        number="03",
        title="Coberturas",
        summary="Caimento e calha resolvidos antes da primeira chuva.",
        detail=(
            "Cobertura mal executada aparece na primeira chuva forte. Definimos caimento, "
            "posição de calha e rufo, e o tipo de telha em função do vão e da insolação do local."
        ),
        applications=("Garagem", "Área de serviço", "Área gourmet", "Estacionamento"),
        materials=("Telha termoacústica", "Telha galvanizada", "Policarbonato", "Estrutura tubular"),
        whatsapp_subject="uma cobertura metálica",
    ),
    Service(
        slug="escadas",
        number="04",
        title="Escadas",
        summary="Degrau regular, piso certo para o ambiente.",
        detail=(
            "Escada é item de segurança. Trabalhamos com altura e profundidade de degrau "
            "regulares ao longo de todo o lance e definimos o tipo de piso conforme o ambiente "
            "seja interno, externo ou de uso industrial."
        ),
        applications=("Interna", "Externa", "Acesso técnico", "Marinheiro"),
        materials=("Chapa xadrez", "Grade de piso", "Degrau em madeira", "Viga central"),
        whatsapp_subject="uma escada metálica",
    ),
    Service(
        slug="guarda-corpos",
        number="05",
        title="Corrimãos e Guarda-corpos",
        summary="Altura e espaçamento dentro da norma.",
        detail=(
            "Guarda-corpo existe para impedir queda. Respeitamos altura minima, espaçamento "
            "entre elementos e ancoragem adequada ao substrato, sem abrir mao do acabamento."
        ),
        applications=("Sacada", "Mezanino", "Escada", "Rampa de acesso"),
        materials=("Inox", "Aço carbono pintado", "Vidro com ferragem", "Cabo de aço"),
        whatsapp_subject="um guarda-corpo ou corrimão",
    ),
    Service(
        slug="grades",
        number="06",
        title="Grades e Proteções",
        summary="Proteção com fixação que não cede.",
        detail=(
            "Proteção só cumpre a função se a fixação acompanhar a resistência da grade. "
            "Executamos ancoragem na alvenaria ou estrutura e tratamento contra corrosao."
        ),
        applications=("Janela", "Porta", "Muro", "Área técnica"),
        materials=("Barra chata", "Tubo quadrado", "Ferro redondo", "Tela metálica"),
        whatsapp_subject="grades de proteção",
    ),
    Service(
        slug="mezaninos",
        number="07",
        title="Mezaninos",
        summary="Mais área útil sem obra civil pesada.",
        detail=(
            "Mezanino multiplica área útil sem obra civil pesada. O dimensionamento considera "
            "a carga que o piso vai receber, o vão livre desejado e os pontos de apoio existentes."
        ),
        applications=("Estoque", "Escritorio", "Loja", "Área industrial"),
        materials=("Perfil I", "Chapa xadrez", "Laje steel deck", "Coluna tubular"),
        whatsapp_subject="um mezanino",
    ),
    Service(
        slug="fachadas",
        number="08",
        title="Fachadas e Letreiros",
        summary="Estrutura de sustentação para painel e letreiro.",
        detail=(
            "A parte que ninguém vê é a que segura o letreiro no lugar. Fabricamos e "
            "instalamos a estrutura de sustentação de painéis e fachadas comerciais, "
            "com ancoragem dimensionada para o peso do painel e para o vento."
        ),
        applications=("Fachada comercial", "Painel de loja", "Totem", "Suporte de letreiro"),
        materials=("Perfil tubular", "Cantoneira", "Chumbador", "Tratamento anticorrosivo"),
        whatsapp_subject="uma estrutura para fachada ou letreiro",
    ),
    Service(
        slug="sob-medida",
        number="09",
        title="Projetos Sob Medida",
        summary="Quando não existe solução pronta.",
        detail=(
            "Quando não existe solução pronta, desenvolvemos a peça a partir da medida do local "
            "e da função que ela precisa cumprir. Traga a ideia, o croqui ou até uma foto."
        ),
        applications=("Suportes", "Bancadas", "Móveis metálicos", "Adaptacoes"),
        materials=("Definido por projeto",),
        whatsapp_subject="um projeto sob medida",
    ),
)


@dataclass(frozen=True)
class Differential:
    key: str
    title: str
    text: str


DIFFERENTIALS: tuple = (
    Differential("medida", "Medida tirada no local",
                 "Nada sai de um modelo padrão."),
    Differential("resistencia", "Perfil escolhido pelo esforço",
                 "Não pelo que sobrou no estoque."),
    Differential("acabamento", "Acabamento incluso",
                 "Solda esmerilhada, tratada e pintada."),
    Differential("atendimento", "Você fala com quem fabrica",
                 "Sem intermediário no meio do caminho."),
    Differential("prazo", "Prazo fechado junto com o valor",
                 "Antes de qualquer compromisso."),
    Differential("processo", "Da medição à instalação",
                 "Você sabe em que etapa seu projeto está."),
)


@dataclass(frozen=True)
class ProcessStep:
    number: str
    title: str
    text: str


PROCESS: tuple = (
    ProcessStep("01", "Conversa", "Uma foto ou um croqui já bastam."),
    ProcessStep("02", "Medição", "Vamos ao local medir e avaliar a fixação."),
    ProcessStep("03", "Proposta", "Solução, material, prazo e valor."),
    ProcessStep("04", "Fabricação", "Corte, montagem, solda e acabamento."),
    ProcessStep("05", "Instalação", "Montagem no local e ajuste final."),
)
