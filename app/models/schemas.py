"""Validacao do pedido de orcamento.

A validacao vive aqui, no servidor. O JavaScript do formulario apenas espelha
estas regras para dar feedback imediato -- nunca as substitui.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator

PHONE_RE = re.compile(r"\D")

SERVICE_SLUGS = {
    "estruturas", "portoes", "coberturas", "escadas",
    "guarda-corpos", "grades", "mezaninos", "sob-medida", "outro",
}

DEADLINES = {"urgente", "30-dias", "60-dias", "sem-pressa", "nao-sei"}


class QuoteRequest(BaseModel):
    service: str = Field(..., description="Slug do serviço desejado")
    description: str = Field(..., min_length=10, max_length=3000)
    measurements: str = Field("", max_length=300)
    deadline: str = Field("nao-sei")
    name: str = Field(..., min_length=2, max_length=120)
    whatsapp: str = Field(..., min_length=8, max_length=30)
    city: str = Field(..., min_length=2, max_length=120)
    attachments: list[str] = Field(default_factory=list)

    # --------------------------------------------------------------- validadores
    @field_validator("service")
    @classmethod
    def _service_known(cls, v: str) -> str:
        if v not in SERVICE_SLUGS:
            raise ValueError("Selecione um tipo de serviço da lista.")
        return v

    @field_validator("deadline")
    @classmethod
    def _deadline_known(cls, v: str) -> str:
        return v if v in DEADLINES else "nao-sei"

    @field_validator("whatsapp")
    @classmethod
    def _phone_ok(cls, v: str) -> str:
        digits = PHONE_RE.sub("", v)
        if not 10 <= len(digits) <= 13:
            raise ValueError("Informe um WhatsApp valido com DDD, ex.: (65) 99999-9999.")
        return digits

    @field_validator("name")
    @classmethod
    def _name_ok(cls, v: str) -> str:
        v = " ".join(v.split())
        if not any(c.isalpha() for c in v):
            raise ValueError("Informe seu nome.")
        return v

    def to_record(self) -> dict:
        data = self.model_dump()
        data["received_at"] = datetime.now(timezone.utc).isoformat()
        return data


# Mensagens em portugues para os erros mais comuns do pydantic.
FIELD_LABELS = {
    "service": "Tipo de serviço",
    "description": "Descrição do projeto",
    "measurements": "Medidas aproximadas",
    "deadline": "Prazo desejado",
    "name": "Nome",
    "whatsapp": "WhatsApp",
    "city": "Cidade",
}

DEFAULT_MESSAGES = {
    "service": "Escolha o tipo de serviço para continuarmos.",
    "description": "Conte em algumas linhas o que você precisa (mínimo 10 caracteres).",
    "name": "Informe seu nome para sabermos com quem falamos.",
    "whatsapp": "Informe seu WhatsApp para continuarmos.",
    "city": "Informe a cidade onde o serviço será executado.",
}
