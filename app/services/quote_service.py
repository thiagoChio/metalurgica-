"""Caso de uso: registrar um pedido de orcamento.

Orquestra validacao, anexos, persistencia e notificacao. O router HTTP nao
conhece nenhum desses detalhes.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.models.schemas import QuoteRequest
from app.services.notifier import Notifier
from app.services.storage import AttachmentStore, QuoteRepository


@dataclass(frozen=True)
class QuoteResult:
    protocol: str


class QuoteService:
    def __init__(self, repository: QuoteRepository, attachments: AttachmentStore, notifier: Notifier) -> None:
        self._repository = repository
        self._attachments = attachments
        self._notifier = notifier

    def store_attachments(self, files) -> list[str]:
        saved: list[str] = []
        for item in files or []:
            name = self._attachments.save(item.filename, item.content_type, item.data)
            if name:
                saved.append(name)
        return saved

    def register(self, request: QuoteRequest) -> QuoteResult:
        record = request.to_record()
        protocol = self._repository.save(record)
        self._notifier.notify(protocol, record)
        return QuoteResult(protocol=protocol)
