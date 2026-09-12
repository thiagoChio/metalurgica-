"""Gerador de desenhos tecnicos em SVG.

Enquanto a empresa nao tem fotografia propria, o site nao usa banco de imagens
generico: cada projeto e representado por um desenho tecnico gerado em codigo,
no mesmo vocabulario visual do restante do site (planta industrial, cotas,
carimbo de prancha).

Vantagens: peso irrisorio, nitidez em qualquer tela, zero risco de licenca e
nenhuma chance de parecer template. Quando a foto real existir, basta popular
`Project.images` e o desenho deixa de ser usado automaticamente.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class BlueprintPalette:
    background: str = "#0A0C22"
    grid: str = "#171B3F"
    grid_strong: str = "#232858"
    line: str = "#A7ADC4"
    line_strong: str = "#E6E8F0"
    accent: str = "#F4C93E"      # dourado do monograma
    dim: str = "#6E748F"


class BlueprintRenderer:
    """Desenha um SVG de prancha tecnica para uma categoria de projeto."""

    WIDTH = 1200
    HEIGHT = 900

    def __init__(self, palette: BlueprintPalette | None = None) -> None:
        self.palette = palette or BlueprintPalette()

    # ------------------------------------------------------------------ publico
    def render(self, slug: str, category: str, title: str) -> str:
        seed = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
        drawing = self._drawing_for(category, seed)
        return self._document(drawing, category, title, slug)

    # ----------------------------------------------------------------- privados
    def _drawing_for(self, category: str, seed: int) -> str:
        table = {
            "Coberturas": self._roof,
            "Portões": self._gate,
            "Escadas": self._stair,
            "Guarda-corpos": self._railing,
            "Mezaninos": self._mezzanine,
            "Estruturas": self._frame,
            "Grades": self._grid_panel,
            "Sob medida": self._bench,
        }
        return table.get(category, self._frame)(seed)

    def _document(self, drawing: str, category: str, title: str, slug: str) -> str:
        p = self.palette
        code = slug.upper().replace("-", ".")[:18]
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.WIDTH} {self.HEIGHT}" role="img" aria-label="Desenho tecnico ilustrativo: {title}">
  <defs>
    <pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="{p.grid}" stroke-width="1"/>
    </pattern>
    <pattern id="G" width="200" height="200" patternUnits="userSpaceOnUse">
      <path d="M200 0H0V200" fill="none" stroke="{p.grid_strong}" stroke-width="1"/>
    </pattern>
    <linearGradient id="vig" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#141838"/>
      <stop offset="100%" stop-color="#080A1C"/>
    </linearGradient>
  </defs>
  <rect width="{self.WIDTH}" height="{self.HEIGHT}" fill="url(#vig)"/>
  <rect width="{self.WIDTH}" height="{self.HEIGHT}" fill="url(#g)"/>
  <rect width="{self.WIDTH}" height="{self.HEIGHT}" fill="url(#G)"/>
  <g transform="translate(0,0)">{drawing}</g>
  <g font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="18" fill="{p.dim}" letter-spacing="2">
    <rect x="60" y="{self.HEIGHT-130}" width="480" height="70" fill="none" stroke="{p.grid_strong}"/>
    <line x1="60" y1="{self.HEIGHT-95}" x2="540" y2="{self.HEIGHT-95}" stroke="{p.grid_strong}"/>
    <text x="76" y="{self.HEIGHT-105}" fill="{p.line}">{category.upper()}</text>
    <text x="76" y="{self.HEIGHT-70}" font-size="15">REF {code}</text>
    <text x="{self.WIDTH-60}" y="{self.HEIGHT-70}" text-anchor="end" font-size="15" fill="{p.dim}">DESENHO ILUSTRATIVO</text>
  </g>
</svg>"""

    # ------------------------------------------------------------- geometrias
    def _roof(self, seed: int) -> str:
        p = self.palette
        bays = 4 + seed % 3
        step = 900 // bays
        posts = "".join(
            f'<line x1="{160+i*step}" y1="{300+i*14}" x2="{160+i*step}" y2="620" stroke="{p.line}" stroke-width="4"/>'
            for i in range(bays + 1)
        )
        purlins = "".join(
            f'<line x1="160" y1="{318+i*40}" x2="{160+bays*step}" y2="{318+i*40+bays*14}" stroke="{p.line}" stroke-width="1.5" opacity=".5"/>'
            for i in range(3)
        )
        return f"""
    <line x1="160" y1="300" x2="{160+bays*step}" y2="{300+bays*14}" stroke="{p.line_strong}" stroke-width="6"/>
    <line x1="160" y1="286" x2="{160+bays*step}" y2="{286+bays*14}" stroke="{p.accent}" stroke-width="2" opacity=".7"/>
    {purlins}{posts}
    <line x1="160" y1="620" x2="{160+bays*step}" y2="620" stroke="{p.dim}" stroke-width="2" stroke-dasharray="10 8"/>
    {self._dim_h(160, 160+bays*step, 690, "VAO LIVRE")}
    {self._dim_v(620, 300, 110, "H")}"""

    def _gate(self, seed: int) -> str:
        p = self.palette
        slats = 12 + seed % 6
        gap = 640 // slats
        bars = "".join(
            f'<rect x="{250+i*gap}" y="250" width="{max(6,gap-10)}" height="420" fill="none" stroke="{p.line}" stroke-width="2"/>'
            for i in range(slats)
        )
        return f"""
    <rect x="230" y="230" width="700" height="460" fill="none" stroke="{p.line_strong}" stroke-width="6"/>
    {bars}
    <line x1="230" y1="460" x2="930" y2="460" stroke="{p.accent}" stroke-width="2" opacity=".6"/>
    <circle cx="880" cy="460" r="16" fill="none" stroke="{p.accent}" stroke-width="3"/>
    {self._dim_h(230, 930, 740, "LARGURA DO VAO")}
    {self._dim_v(690, 230, 180, "ALTURA")}"""

    def _stair(self, seed: int) -> str:
        p = self.palette
        steps = 8 + seed % 4
        tread, riser = 62, 44
        path = []
        x, y = 250, 690
        for _ in range(steps):
            path.append(f"L{x} {y-riser}")
            y -= riser
            path.append(f"L{x+tread} {y}")
            x += tread
        stringer = f'<path d="M250 690 {"".join(path)}" fill="none" stroke="{p.line_strong}" stroke-width="5"/>'
        rail = f'<line x1="250" y1="560" x2="{x}" y2="{y-130}" stroke="{p.accent}" stroke-width="3" opacity=".8"/>'
        posts = "".join(
            f'<line x1="{250+i*tread*3}" y1="{690-i*riser*3}" x2="{250+i*tread*3}" y2="{560-i*riser*3}" stroke="{p.line}" stroke-width="2"/>'
            for i in range(steps // 3 + 1)
        )
        return f"{stringer}{rail}{posts}{self._dim_h(250, x, 760, 'PROJECAO')}{self._dim_v(690, y, 190, 'DESNIVEL')}"

    def _railing(self, seed: int) -> str:
        p = self.palette
        n = 14 + seed % 8
        gap = 700 // n
        posts = "".join(
            f'<line x1="{240+i*gap}" y1="330" x2="{240+i*gap}" y2="620" stroke="{p.line}" stroke-width="3"/>'
            for i in range(n + 1)
        )
        return f"""
    <line x1="230" y1="320" x2="950" y2="320" stroke="{p.line_strong}" stroke-width="8"/>
    <line x1="230" y1="470" x2="950" y2="470" stroke="{p.line}" stroke-width="3"/>
    {posts}
    <line x1="220" y1="620" x2="960" y2="620" stroke="{p.dim}" stroke-width="6"/>
    <line x1="220" y1="640" x2="960" y2="640" stroke="{p.accent}" stroke-width="2" opacity=".5" stroke-dasharray="4 10"/>
    {self._dim_v(620, 320, 170, "ALTURA MIN.")}
    {self._dim_h(240, 240+gap, 700, "ESPACAMENTO")}"""

    def _mezzanine(self, seed: int) -> str:
        p = self.palette
        cols = 3 + seed % 3
        step = 760 // cols
        columns = "".join(
            f'<rect x="{200+i*step-10}" y="420" width="20" height="270" fill="none" stroke="{p.line}" stroke-width="3"/>'
            for i in range(cols + 1)
        )
        return f"""
    <rect x="180" y="390" width="800" height="30" fill="none" stroke="{p.line_strong}" stroke-width="5"/>
    <line x1="180" y1="378" x2="980" y2="378" stroke="{p.accent}" stroke-width="2" opacity=".7"/>
    {columns}
    <line x1="160" y1="690" x2="1000" y2="690" stroke="{p.dim}" stroke-width="4"/>
    <line x1="160" y1="230" x2="1000" y2="230" stroke="{p.dim}" stroke-width="2" stroke-dasharray="12 8"/>
    {self._dim_v(690, 390, 120, "PE-DIREITO LIVRE")}
    {self._dim_h(200, 200+step, 750, "MODULO")}"""

    def _frame(self, seed: int) -> str:
        p = self.palette
        braces = "".join(
            f'<line x1="{260+i*220}" y1="620" x2="{480+i*220}" y2="360" stroke="{p.line}" stroke-width="1.5" opacity=".55"/>'
            f'<line x1="{480+i*220}" y1="620" x2="{260+i*220}" y2="360" stroke="{p.line}" stroke-width="1.5" opacity=".55"/>'
            for i in range(2 + seed % 2)
        )
        return f"""
    <path d="M260 620 L260 360 L600 250 L940 360 L940 620" fill="none" stroke="{p.line_strong}" stroke-width="6"/>
    <line x1="260" y1="360" x2="940" y2="360" stroke="{p.line}" stroke-width="3"/>
    <line x1="600" y1="250" x2="600" y2="360" stroke="{p.accent}" stroke-width="3"/>
    {braces}
    <line x1="220" y1="620" x2="980" y2="620" stroke="{p.dim}" stroke-width="4"/>
    {self._dim_h(260, 940, 700, "VAO ESTRUTURAL")}
    {self._dim_v(620, 250, 170, "ALTURA")}"""

    def _grid_panel(self, seed: int) -> str:
        p = self.palette
        cols, rows = 6 + seed % 4, 4
        w, h = 620, 380
        x0, y0 = 290, 260
        v = "".join(
            f'<line x1="{x0+i*w/cols}" y1="{y0}" x2="{x0+i*w/cols}" y2="{y0+h}" stroke="{p.line}" stroke-width="2"/>'
            for i in range(cols + 1)
        )
        hz = "".join(
            f'<line x1="{x0}" y1="{y0+i*h/rows}" x2="{x0+w}" y2="{y0+i*h/rows}" stroke="{p.line}" stroke-width="2" opacity=".6"/>'
            for i in range(rows + 1)
        )
        return f"""
    <rect x="{x0-20}" y="{y0-20}" width="{w+40}" height="{h+40}" fill="none" stroke="{p.line_strong}" stroke-width="6"/>
    {v}{hz}
    <rect x="{x0-20}" y="{y0-20}" width="{w+40}" height="{h+40}" fill="none" stroke="{p.accent}" stroke-width="1" opacity=".4" stroke-dasharray="8 12"/>
    {self._dim_h(x0-20, x0+w+20, y0+h+90, "LARGURA")}
    {self._dim_v(y0+h+20, y0-20, 230, "ALTURA")}"""

    def _bench(self, seed: int) -> str:
        p = self.palette
        legs = "".join(
            f'<line x1="{x}" y1="380" x2="{x}" y2="640" stroke="{p.line}" stroke-width="5"/>' for x in (280, 920)
        )
        return f"""
    <rect x="250" y="340" width="700" height="40" fill="none" stroke="{p.line_strong}" stroke-width="5"/>
    <line x1="250" y1="330" x2="950" y2="330" stroke="{p.accent}" stroke-width="2" opacity=".7"/>
    {legs}
    <rect x="280" y="530" width="640" height="20" fill="none" stroke="{p.line}" stroke-width="3" opacity=".7"/>
    <line x1="230" y1="640" x2="970" y2="640" stroke="{p.dim}" stroke-width="4"/>
    {self._dim_h(250, 950, 700, "COMPRIMENTO")}
    {self._dim_v(640, 340, 190, "ALTURA UTIL")}"""

    # ------------------------------------------------------------------ cotas
    def _dim_h(self, x1: int, x2: int, y: int, label: str) -> str:
        p = self.palette
        return f"""
    <g stroke="{p.dim}" fill="{p.dim}" font-family="ui-monospace,monospace" font-size="15" letter-spacing="1.5">
      <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke-width="1"/>
      <line x1="{x1}" y1="{y-8}" x2="{x1}" y2="{y+8}" stroke-width="1"/>
      <line x1="{x2}" y1="{y-8}" x2="{x2}" y2="{y+8}" stroke-width="1"/>
      <text x="{(x1+x2)//2}" y="{y-14}" text-anchor="middle" stroke="none">{label}</text>
    </g>"""

    def _dim_v(self, y1: int, y2: int, x: int, label: str) -> str:
        p = self.palette
        mid = (y1 + y2) // 2
        return f"""
    <g stroke="{p.dim}" fill="{p.dim}" font-family="ui-monospace,monospace" font-size="15" letter-spacing="1.5">
      <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke-width="1"/>
      <line x1="{x-8}" y1="{y1}" x2="{x+8}" y2="{y1}" stroke-width="1"/>
      <line x1="{x-8}" y1="{y2}" x2="{x+8}" y2="{y2}" stroke-width="1"/>
      <text x="{x-14}" y="{mid}" text-anchor="middle" stroke="none" transform="rotate(-90 {x-14} {mid})">{label}</text>
    </g>"""


RENDERER = BlueprintRenderer()
