"""Configuracao da aplicacao (12-factor: tudo por variavel de ambiente)."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="SITE_", extra="ignore")

    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000

    # Notas de pendência ("[ COMPLETAR ]") aparecem só em desenvolvimento.
    # Ao apresentar para o cliente, rode com SITE_DEBUG=false e elas somem.
    # Para forçar, use SITE_DRAFT_NOTES=true/false.
    draft_notes: bool | None = None

    # Armazenamento dos pedidos de orcamento
    quotes_dir: Path = BASE_DIR / "data" / "quotes"
    uploads_dir: Path = BASE_DIR / "data" / "uploads"
    max_upload_mb: int = 10
    allowed_upload_types: tuple = ("image/jpeg", "image/png", "image/webp", "application/pdf")

    # Notificacao por e-mail (opcional). Sem SMTP configurado, apenas registra em disco.
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    notify_to: str = ""

    @property
    def show_draft_notes(self) -> bool:
        return self.debug if self.draft_notes is None else self.draft_notes

    @property
    def templates_dir(self) -> Path:
        return BASE_DIR / "templates"

    @property
    def static_dir(self) -> Path:
        return BASE_DIR / "static"


settings = Settings()
settings.quotes_dir.mkdir(parents=True, exist_ok=True)
settings.uploads_dir.mkdir(parents=True, exist_ok=True)
