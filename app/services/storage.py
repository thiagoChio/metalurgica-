"""Persistencia dos pedidos de orcamento.

Implementacao em arquivo JSONL: zero dependencia de banco, facil de migrar.
A interface `QuoteRepository` permite trocar por Postgres/Sheets sem tocar no
resto da aplicacao.
"""

from __future__ import annotations

import json
import secrets
import unicodedata
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path


class QuoteRepository(ABC):
    @abstractmethod
    def save(self, record: dict) -> str:
        """Persiste o pedido e devolve o protocolo."""

    @abstractmethod
    def list_all(self) -> list[dict]:
        """Lista os pedidos recebidos (uso interno / painel futuro)."""


class JsonlQuoteRepository(QuoteRepository):
    def __init__(self, directory: Path) -> None:
        self._dir = directory
        self._dir.mkdir(parents=True, exist_ok=True)

    @property
    def _file(self) -> Path:
        return self._dir / "quotes.jsonl"

    def save(self, record: dict) -> str:
        protocol = self._new_protocol()
        record = {"protocol": protocol, **record}
        with self._file.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return protocol

    def list_all(self) -> list[dict]:
        if not self._file.exists():
            return []
        with self._file.open(encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]

    @staticmethod
    def _new_protocol() -> str:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
        return f"{stamp}-{secrets.token_hex(3).upper()}"


class AttachmentStore:
    """Grava anexos enviados pelo formulario, com nome sanitizado."""

    def __init__(self, directory: Path, allowed_types: tuple, max_bytes: int) -> None:
        self._dir = directory
        self._allowed = allowed_types
        self._max = max_bytes
        self._dir.mkdir(parents=True, exist_ok=True)

    def accepts(self, content_type: str) -> bool:
        return content_type in self._allowed

    def save(self, filename: str, content_type: str, data: bytes) -> str | None:
        if not data or not self.accepts(content_type) or len(data) > self._max:
            return None
        safe = self._sanitize(filename)
        target = self._dir / f"{secrets.token_hex(4)}_{safe}"
        target.write_bytes(data)
        return target.name

    @staticmethod
    def _sanitize(filename: str) -> str:
        base = Path(filename).name
        normalized = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode()
        cleaned = "".join(c for c in normalized if c.isalnum() or c in "._-")
        return cleaned[-80:] or "arquivo"
