"""Rotas de pagina e de midia gerada."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.content import CONTENT
from app.content.portfolio import PROJECTS
from app.services.blueprint import RENDERER
from app.services.seo import build_graph

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))
templates.env.globals["content"] = CONTENT
templates.env.globals["company"] = CONTENT.company
templates.env.globals["draft"] = settings.show_draft_notes


@router.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "content": CONTENT,
            "structured_data": build_graph(CONTENT.company, CONTENT.services, CONTENT.faq),
            "services_json": _services_payload(),
            "projects_json": _projects_payload(),
        },
    )


# Cada servico e representado pela mesma familia de desenho tecnico do portfolio.
SERVICE_DRAWINGS = {
    "estruturas": "Estruturas", "portoes": "Portões", "coberturas": "Coberturas",
    "escadas": "Escadas", "guarda-corpos": "Guarda-corpos", "grades": "Grades",
    "mezaninos": "Mezaninos", "fachadas": "Estruturas", "sob-medida": "Sob medida",
}


@router.get("/media/blueprint/{slug}.svg")
async def blueprint(slug: str) -> Response:
    if slug.startswith("servico-"):
        chave = slug.removeprefix("servico-")
        servico = CONTENT.service_by_slug(chave)
        categoria = SERVICE_DRAWINGS.get(chave, "Estruturas")
        svg = RENDERER.render(slug, categoria, servico.title if servico else chave)
    else:
        projeto = next((p for p in PROJECTS if p.slug == slug), None)
        svg = (RENDERER.render(projeto.slug, projeto.category, projeto.title)
               if projeto else RENDERER.render(slug, "Estruturas", slug))
    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": "public, max-age=604800"},
    )


@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots() -> str:
    return f"User-agent: *\nAllow: /\nSitemap: {CONTENT.company.domain}/sitemap.xml\n"


@router.get("/sitemap.xml")
async def sitemap() -> Response:
    base = CONTENT.company.domain
    urls = "".join(f"<url><loc>{base}/</loc><priority>1.0</priority></url>")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>"
    )
    return Response(content=xml, media_type="application/xml")


# ---------------------------------------------------------------- payloads
def _services_payload() -> dict:
    """Conteudo dos servicos entregue ao modal, ja renderizado pelo servidor."""
    return {
        s.slug: {
            "kind": "servico",
            "number": s.number,
            "title": s.title,
            "summary": s.summary,
            "detail": s.detail,
            "applications": list(s.applications),
            "materials": list(s.materials),
            "whatsapp": CONTENT.whatsapp_for_service(s.slug),
        }
        for s in CONTENT.services
    }


def _projects_payload() -> dict:
    return {
        p.slug: {
            "kind": "projeto",
            "title": p.title,
            "category": p.category,
            "location": p.location,
            "summary": p.summary,
            "purpose": p.purpose,
            "materials": list(p.materials),
            "gallery": list(p.gallery),
            "is_placeholder": p.is_placeholder,
            "whatsapp": CONTENT.whatsapp_for_service(),
        }
        for p in CONTENT.projects
    }
