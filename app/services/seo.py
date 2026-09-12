"""Dados estruturados (schema.org).

Regra: um campo so entra no JSON-LD se contiver dado real. Placeholder no
schema e pior que schema ausente -- o Google indexa a informacao falsa.
"""

from __future__ import annotations


def _real(value: str) -> bool:
    return bool(value) and not value.strip().startswith("[")


def build_local_business(company, services) -> dict:
    data: dict = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "additionalType": "https://schema.org/HomeAndConstructionBusiness",
        "description": company.meta_description,
        "url": company.domain,
    }

    if _real(company.name):
        data["name"] = company.name
    if _real(company.email):
        data["email"] = company.email
    if _real(company.phone_display):
        data["telephone"] = company.phone_display

    address = {}
    if _real(company.address):
        address["streetAddress"] = company.address
    if _real(company.city):
        address["addressLocality"] = company.city
    if _real(company.state):
        address["addressRegion"] = company.state
    if address:
        address["@type"] = "PostalAddress"
        address["addressCountry"] = "BR"
        data["address"] = address

    if _real(company.service_area):
        data["areaServed"] = company.service_area

    perfis = [s.url for s in company.socials if _real(s.url)]
    if perfis:
        data["sameAs"] = perfis

    data["hasOfferCatalog"] = {
        "@type": "OfferCatalog",
        "name": "Servicos",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s.title, "description": s.summary}}
            for s in services
        ],
    }
    return data


def build_faq(faq_items) -> dict | None:
    """So publica FAQ estruturada com respostas definitivas (sem [CONFIRMAR])."""
    prontos = [item for item in faq_items if not item.needs_review]
    if not prontos:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item.question,
                "acceptedAnswer": {"@type": "Answer", "text": item.answer},
            }
            for item in prontos
        ],
    }


def build_graph(company, services, faq_items) -> list[dict]:
    grafo = [build_local_business(company, services)]
    faq = build_faq(faq_items)
    if faq:
        grafo.append(faq)
    return grafo
