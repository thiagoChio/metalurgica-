"""API do formulário de orçamento."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.config import settings
from app.models.schemas import DEFAULT_MESSAGES, QuoteRequest
from app.services.notifier import build_notifier
from app.services.quote_service import QuoteService
from app.services.storage import AttachmentStore, JsonlQuoteRepository

router = APIRouter(prefix="/api")

_service = QuoteService(
    repository=JsonlQuoteRepository(settings.quotes_dir),
    attachments=AttachmentStore(
        settings.uploads_dir,
        settings.allowed_upload_types,
        settings.max_upload_mb * 1024 * 1024,
    ),
    notifier=build_notifier(settings),
)


@dataclass
class _Incoming:
    filename: str
    content_type: str
    data: bytes


def _translate(error: ValidationError) -> dict[str, str]:
    """Converte erros do pydantic em mensagens acionaveis, campo a campo."""
    saida: dict[str, str] = {}
    for item in error.errors():
        campo = str(item["loc"][0]) if item["loc"] else "geral"
        if campo in DEFAULT_MESSAGES and item["type"] in {"missing", "string_too_short"}:
            saida[campo] = DEFAULT_MESSAGES[campo]
        else:
            mensagem = item.get("msg", "")
            saida[campo] = mensagem.replace("Value error, ", "") or DEFAULT_MESSAGES.get(
                campo, "Revise este campo."
            )
    return saida


@router.post("/orcamento")
async def create_quote(
    service: str = Form(""),
    description: str = Form(""),
    measurements: str = Form(""),
    deadline: str = Form("nao-sei"),
    name: str = Form(""),
    whatsapp: str = Form(""),
    city: str = Form(""),
    files: list[UploadFile] = File(default=[]),
) -> JSONResponse:
    recebidos = [
        _Incoming(f.filename or "arquivo", f.content_type or "", await f.read())
        for f in files
        if f is not None and f.filename
    ]
    anexos = _service.store_attachments(recebidos)

    try:
        pedido = QuoteRequest(
            service=service,
            description=description,
            measurements=measurements,
            deadline=deadline,
            name=name,
            whatsapp=whatsapp,
            city=city,
            attachments=anexos,
        )
    except ValidationError as erro:
        return JSONResponse(status_code=422, content={"ok": False, "errors": _translate(erro)})

    resultado = _service.register(pedido)
    return JSONResponse(
        {
            "ok": True,
            "protocol": resultado.protocol,
            "message": "Recebemos sua solicitação. Nossa equipe entrará em contato em breve.",
        }
    )
