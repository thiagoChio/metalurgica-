/**
 * HERO — faíscas de solda sobre a fotografia da obra.
 *
 * A versão anterior deste módulo desenhava uma treliça em canvas porque não
 * havia fotografia da empresa. Agora existe: a foto do hero JÁ é uma estrutura
 * real da Correa Metalúrgica, e redesenhar uma por cima seria ruído.
 *
 * Ficou só o que a foto não tem e a marca pede: as faíscas douradas do selo,
 * caindo devagar em dois pontos de solda. Custa ~2 KB e para de rodar assim
 * que o hero sai da tela.
 */

const DOURADO = '#F4C93E';
const QUENTE = '#FFE7A8';

class Spark {
  constructor(x, y) {
    const angulo = Math.random() * Math.PI * 2;
    const velocidade = 0.4 + Math.random() * 2.2;
    this.x = x; this.y = y;
    this.vx = Math.cos(angulo) * velocidade;
    this.vy = Math.sin(angulo) * velocidade - 0.6;
    this.vida = 1;
    this.decaimento = 0.010 + Math.random() * 0.020;
  }

  atualizar() {
    this.x += this.vx; this.y += this.vy;
    this.vy += 0.05;      // gravidade
    this.vx *= 0.985;     // arrasto
    this.vida -= this.decaimento;
  }

  desenhar(ctx) {
    if (this.vida <= 0) return;
    ctx.globalAlpha = Math.max(this.vida, 0) * 0.9;
    ctx.fillStyle = this.vida > 0.62 ? QUENTE : DOURADO;
    ctx.fillRect(this.x, this.y, 1.7, 1.7);
    ctx.globalAlpha = 1;
  }
}

/** Ponto onde a solda acontece, em fração da largura/altura do hero. */
class Fonte {
  constructor(fx, fy, intervalo) {
    this.fx = fx; this.fy = fy; this.intervalo = intervalo; this.fase = Math.random() * 400;
  }

  ativa(quadro) {
    // liga e desliga: uma solda real é intermitente, não um jorro contínuo
    const ciclo = (quadro + this.fase) % this.intervalo;
    return ciclo < this.intervalo * 0.34;
  }
}

export class HeroCanvas {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d', { alpha: true });
    this.sparks = [];
    this.quadro = 0;
    this.rodando = false;
    this.fontes = [new Fonte(0.72, 0.46, 300), new Fonte(0.88, 0.62, 420)];
  }

  init() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    this.#dimensionar();
    window.addEventListener('resize', () => this.#dimensionar(), { passive: true });

    // Fora da tela o laço para: nada de gastar bateria animando o invisível.
    new IntersectionObserver(([entrada]) => {
      this.rodando = entrada.isIntersecting;
      if (this.rodando) requestAnimationFrame(this.#passo);
    }, { threshold: 0.02 }).observe(this.canvas);
  }

  #dimensionar() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const r = this.canvas.getBoundingClientRect();
    this.tamanho = { largura: r.width, altura: r.height };
    this.canvas.width = Math.round(r.width * dpr);
    this.canvas.height = Math.round(r.height * dpr);
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  #passo = () => {
    if (!this.rodando) return;
    this.quadro += 1;
    const { largura, altura } = this.tamanho;

    this.fontes.forEach((fonte) => {
      if (!fonte.ativa(this.quadro) || this.sparks.length > 130) return;
      const x = largura * fonte.fx;
      const y = altura * fonte.fy;
      for (let i = 0; i < 2; i += 1) this.sparks.push(new Spark(x, y));
    });

    this.sparks = this.sparks.filter((s) => { s.atualizar(); return s.vida > 0; });

    const { ctx } = this;
    ctx.clearRect(0, 0, largura, altura);

    this.fontes.forEach((fonte) => {
      if (!fonte.ativa(this.quadro)) return;
      const x = largura * fonte.fx;
      const y = altura * fonte.fy;
      const brilho = ctx.createRadialGradient(x, y, 0, x, y, 60);
      brilho.addColorStop(0, 'rgba(255, 231, 168, .30)');
      brilho.addColorStop(1, 'rgba(244, 201, 62, 0)');
      ctx.fillStyle = brilho;
      ctx.beginPath(); ctx.arc(x, y, 60, 0, Math.PI * 2); ctx.fill();
    });

    this.sparks.forEach((s) => s.desenhar(ctx));
    requestAnimationFrame(this.#passo);
  };
}
