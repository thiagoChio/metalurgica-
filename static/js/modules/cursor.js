/**
 * Cursor contextual (apenas ponteiro fino).
 * Sobre um projeto diz "Ver projeto"; sobre um servico, "Explorar".
 * Em toque, o modulo nem inicializa.
 */

import { motion } from './motion.js';

export class ContextCursor {
  constructor(node) {
    this.node = node;
    this.label = node?.querySelector('[data-cursor-label]');
    this.pos = { x: 0, y: 0, tx: 0, ty: 0 };
  }

  init() {
    if (!this.node) return;
    if (motion.reduced || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      this.node.remove();
      return;
    }

    window.addEventListener('pointermove', (event) => {
      this.pos.tx = event.clientX;
      this.pos.ty = event.clientY;
    }, { passive: true });

    document.querySelectorAll('[data-cursor-hover]').forEach((target) => {
      target.addEventListener('pointerenter', () => this.#show(target.dataset.cursorHover));
      target.addEventListener('pointerleave', () => this.#hide());
      target.addEventListener('click', () => this.#hide());
    });

    this.#loop();
  }

  #show(text) {
    this.label.textContent = `${text} →`;
    this.node.classList.add('is-active');
  }

  #hide() { this.node.classList.remove('is-active'); }

  #loop = () => {
    this.pos.x += (this.pos.tx - this.pos.x) * 0.18;
    this.pos.y += (this.pos.ty - this.pos.y) * 0.18;
    // `translate` e nao `transform`: o transform pertence ao CSS (escala de entrada).
    this.node.style.translate = `${this.pos.x}px ${this.pos.y}px`;
    requestAnimationFrame(this.#loop);
  };
}
