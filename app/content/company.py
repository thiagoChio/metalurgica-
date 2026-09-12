# -*- coding: utf-8 -*-
"""Dados institucionais da Correa Metalúrgica.

Preenchido a partir do material entregue pela empresa: cartão de visita,
manual de marca e fotos das obras.

O que ainda estiver entre colchetes é dado que NÃO foi confirmado e não
deve ir ao ar antes de checagem.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SocialLink:
    label: str
    url: str
    icon: str


@dataclass(frozen=True)
class Company:
    # ---------------------------------------------------------------- IDENTIDADE
    name: str = "Correa Metalúrgica"
    short_name: str = "CM"
    tagline: str = "Metalúrgica e estruturas metálicas."
    legal_name: str = "[RAZÃO SOCIAL]"
    cnpj: str = "[CNPJ]"

    # ---------------------------------------------------------------- PESSOAS
    owner: str = "Julimar Correa"
    owner_role: str = "Metalúrgico chefe"
    partner: str = "Eliana Imbriani"

    # ---------------------------------------------------------------- CONTATO
    whatsapp_raw: str = "5565996265207"        # 65 99626-5207 — Julimar
    whatsapp_alt_raw: str = "5565993464848"    # 65 99346-4848 — Eliana
    phone_display: str = "(65) 99626-5207"
    phone_alt_display: str = "(65) 99346-4848"
    email: str = "correametalurgicamt@gmail.com"

    # ---------------------------------------------------------------- LOCALIZAÇÃO
    address: str = "Av. Canadá, 800 — Santa Rosa, Cuiabá/MT, 78040-050"
    city: str = "Cuiabá"
    state: str = "MT"
    service_area: str = "Cuiabá, Várzea Grande e região"
    # Embed público do endereço. Troque pelo embed do perfil da empresa no
    # Google Meu Negócio quando ele existir — o marcador fica mais preciso.
    maps_embed_url: str = (
        "https://maps.google.com/maps?q=Av.+Canad%C3%A1,+800,+Santa+Rosa,+Cuiab%C3%A1+-+MT"
        "&z=15&output=embed"
    )

    # ---------------------------------------------------------------- SEO
    domain: str = "https://www.correametalurgica.com.br"
    meta_description: str = (
        "Estruturas metálicas sob medida em Cuiabá e Várzea Grande: coberturas, "
        "portões, grades, escadas e estruturas para fachada. Orçamento pelo WhatsApp."
    )

    socials: tuple = field(
        default_factory=lambda: (
            SocialLink("Instagram", "[INSTAGRAM]", "instagram"),
            SocialLink("Facebook", "[FACEBOOK]", "facebook"),
        )
    )

    # ------------------------------------------------------------------ MÉTODOS
    @property
    def is_whatsapp_configured(self) -> bool:
        return self.whatsapp_raw.isdigit() and len(self.whatsapp_raw) >= 12

    def whatsapp_link(self, message: str) -> str:
        """Monta o link do WhatsApp com mensagem pré-preenchida."""
        from urllib.parse import quote

        if not self.is_whatsapp_configured:
            return "#orcamento"
        return f"https://wa.me/{self.whatsapp_raw}?text={quote(message)}"

    @property
    def has_address(self) -> bool:
        return not self.address.startswith("[")

    @property
    def location_label(self) -> str:
        return f"{self.city}/{self.state}"

    @property
    def visible_socials(self) -> tuple:
        """Rede social só aparece no site quando o perfil real for informado."""
        return tuple(s for s in self.socials if not s.url.startswith("["))


COMPANY = Company()
