/**
 * Preferencia de movimento e revelacao por scroll.
 * Uma unica fonte de verdade: se o usuario pediu menos movimento, nenhum
 * modulo anima. Nao ha excecao "so essa animacao aqui".
 */

const query = window.matchMedia('(prefers-reduced-motion: reduce)');

export const motion = {
  get reduced() { return query.matches; },
  onChange(callback) { query.addEventListener('change', () => callback(query.matches)); },
};

/**
 * Revela elementos ao entrar na viewport.
 * - [data-reveal]        elemento isolado
 * - [data-reveal-group]  filhos revelados em cascata (stagger)
 * - [data-step]          etapas do processo, com a linha se desenhando
 */
export class RevealObserver {
  constructor({ rootMargin = '0px 0px -12% 0px', threshold = 0.15 } = {}) {
    this.observer = new IntersectionObserver(
      (entries) => entries.forEach((entry) => this.#handle(entry)),
      { rootMargin, threshold },
    );
  }

  observe(selector = '[data-reveal], [data-reveal-group], [data-step]') {
    const nodes = document.querySelectorAll(selector);
    if (motion.reduced) { nodes.forEach((node) => node.classList.add('is-in')); return; }
    nodes.forEach((node) => this.observer.observe(node));
  }

  #handle(entry) {
    if (!entry.isIntersecting) return;
    const node = entry.target;
    node.classList.add('is-in');

    if (node.hasAttribute('data-reveal-group')) {
      [...node.children].forEach((child, index) => {
        child.style.transitionDelay = `${Math.min(index * 70, 560)}ms`;
      });
    }
    this.observer.unobserve(node);
  }
}
