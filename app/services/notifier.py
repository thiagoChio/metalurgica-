"""Notificacao de novos orcamentos.

Sem SMTP configurado, o notificador apenas registra em log -- o pedido nunca
se perde, porque ja foi gravado pelo repositorio antes desta etapa.
"""

from __future__ import annotations

import logging
import smtplib
from abc import ABC, abstractmethod
from email.message import EmailMessage

logger = logging.getLogger("metalurgica.notifier")


class Notifier(ABC):
    @abstractmethod
    def notify(self, protocol: str, record: dict) -> None: ...


class LogNotifier(Notifier):
    def notify(self, protocol: str, record: dict) -> None:
        logger.info("Novo orcamento %s de %s (%s) - %s",
                    protocol, record.get("name"), record.get("whatsapp"), record.get("service"))


class SmtpNotifier(Notifier):
    def __init__(self, host: str, port: int, user: str, password: str, to: str) -> None:
        self._host, self._port, self._user, self._password, self._to = host, port, user, password, to

    def notify(self, protocol: str, record: dict) -> None:
        message = EmailMessage()
        message["Subject"] = f"Novo pedido de orcamento {protocol}"
        message["From"] = self._user
        message["To"] = self._to
        message.set_content(self._body(protocol, record))
        try:
            with smtplib.SMTP(self._host, self._port, timeout=15) as smtp:
                smtp.starttls()
                smtp.login(self._user, self._password)
                smtp.send_message(message)
        except Exception:  # noqa: BLE001 - falha de e-mail nao pode derrubar o pedido
            logger.exception("Falha ao enviar e-mail do orcamento %s", protocol)

    @staticmethod
    def _body(protocol: str, record: dict) -> str:
        linhas = [f"Protocolo: {protocol}", ""]
        for chave, rotulo in (
            ("name", "Nome"), ("whatsapp", "WhatsApp"), ("city", "Cidade"),
            ("service", "Servico"), ("measurements", "Medidas"), ("deadline", "Prazo"),
        ):
            linhas.append(f"{rotulo}: {record.get(chave) or '-'}")
        linhas += ["", "Descricao:", record.get("description", "")]
        if record.get("attachments"):
            linhas += ["", "Anexos: " + ", ".join(record["attachments"])]
        return "\n".join(linhas)


def build_notifier(settings) -> Notifier:
    if settings.smtp_host and settings.notify_to:
        return SmtpNotifier(settings.smtp_host, settings.smtp_port,
                            settings.smtp_user, settings.smtp_password, settings.notify_to)
    return LogNotifier()
