"""Camada de conteudo: unico ponto de verdade do texto do site.

`SiteContent` decide o que pode ou nao ir para a tela. A regra central:
conteudo marcado como placeholder NAO e publicado. Isso impede que numeros
inventados ou depoimentos falsos vazem para producao por esquecimento.
"""

from dataclasses import dataclass

from app.content.catalog import DIFFERENTIALS, PROCESS, SERVICES, Service
from app.content.company import COMPANY, Company
from app.content.portfolio import FAQ, PROJECTS, STATS, TESTIMONIALS


@dataclass(frozen=True)
class SiteContent:
    company: Company = COMPANY
    services: tuple = SERVICES
    differentials: tuple = DIFFERENTIALS
    process: tuple = PROCESS
    projects: tuple = PROJECTS

    @property
    def faq(self) -> tuple:
        """Só publica pergunta cuja resposta já foi confirmada pela empresa.

        Uma resposta marcada [CONFIRMAR] no site é pior que pergunta ausente:
        anuncia ao cliente que a empresa não sabe a própria política."""
        return tuple(item for item in FAQ if not item.needs_review)

    @property
    def faq_pendentes(self) -> tuple:
        return tuple(item for item in FAQ if item.needs_review)

    # --------------------------------------------- publicacao condicional
    @property
    def stats(self) -> tuple:
        """Só publica estatísticas se TODAS forem reais."""
        return () if any(s.is_placeholder for s in STATS) else STATS

    @property
    def testimonials(self) -> tuple:
        """Só publica depoimentos reais. Nenhum depoimento e inventado."""
        return tuple(t for t in TESTIMONIALS if not t.is_placeholder)

    @property
    def has_real_projects(self) -> bool:
        return any(not p.is_placeholder for p in self.projects)

    @property
    def project_categories(self) -> tuple:
        vistas: list[str] = []
        for projeto in self.projects:
            if projeto.category not in vistas:
                vistas.append(projeto.category)
        return tuple(vistas)

    def service_by_slug(self, slug: str) -> Service | None:
        return next((s for s in self.services if s.slug == slug), None)

    def whatsapp_for_service(self, slug: str | None = None) -> str:
        servico = self.service_by_slug(slug) if slug else None
        assunto = servico.whatsapp_subject if servico else "um serviço de metalúrgica"
        return self.company.whatsapp_link(
            f"Ola! Vim pelo site e gostaria de solicitar um orçamento para {assunto}."
        )


CONTENT = SiteContent()
