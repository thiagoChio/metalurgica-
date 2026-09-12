/** FAQ acessivel: um item aberto por vez, altura animada por grid-template-rows. */

export class Accordion {
  constructor(root) { this.root = root; }

  init() {
    if (!this.root) return;
    this.triggers = [...this.root.querySelectorAll('.faq__trigger')];
    this.triggers.forEach((trigger) => {
      trigger.addEventListener('click', () => this.#toggle(trigger));
      trigger.addEventListener('keydown', (event) => this.#navigate(event, trigger));
    });
  }

  #toggle(trigger) {
    const open = trigger.getAttribute('aria-expanded') === 'true';
    this.triggers.forEach((other) => this.#set(other, false));
    if (!open) this.#set(trigger, true);
  }

  #set(trigger, open) {
    trigger.setAttribute('aria-expanded', String(open));
    document.getElementById(trigger.getAttribute('aria-controls'))
      ?.classList.toggle('is-open', open);
  }

  #navigate(event, trigger) {
    const keys = { ArrowDown: 1, ArrowUp: -1 };
    if (!(event.key in keys)) return;
    event.preventDefault();
    const index = this.triggers.indexOf(trigger);
    const next = (index + keys[event.key] + this.triggers.length) % this.triggers.length;
    this.triggers[next].focus();
  }
}
