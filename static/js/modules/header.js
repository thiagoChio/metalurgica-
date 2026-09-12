/** Header fixo: estado compactado no scroll, link ativo por secao, menu mobile. */

export class Header {
  constructor(root) {
    this.root = root;
    this.links = [...document.querySelectorAll('[data-nav-link]')];
    this.burger = document.querySelector('[data-burger]');
    this.panel = document.querySelector('[data-mobile-panel]');
    this.lastFocus = null;
  }

  init() {
    this.#watchScroll();
    this.#watchSections();
    this.#watchMenu();
  }

  #watchScroll() {
    let ticking = false;
    const apply = () => {
      this.root.classList.toggle('is-stuck', window.scrollY > 40);
      ticking = false;
    };
    apply();
    window.addEventListener('scroll', () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(apply);
    }, { passive: true });
  }

  #watchSections() {
    const sections = this.links
      .map((link) => document.querySelector(link.getAttribute('href')))
      .filter(Boolean);
    if (!sections.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        this.links.forEach((link) => {
          const active = link.getAttribute('href') === `#${entry.target.id}`;
          link.setAttribute('aria-current', active ? 'true' : 'false');
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });

    sections.forEach((section) => observer.observe(section));
  }

  #watchMenu() {
    if (!this.burger || !this.panel) return;

    const links = [...this.panel.querySelectorAll('[data-mobile-link]')];
    links.forEach((link, index) => { link.style.transitionDelay = `${120 + index * 55}ms`; });

    this.burger.addEventListener('click', () => this.toggle());
    links.forEach((link) => link.addEventListener('click', () => this.close()));

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && this.isOpen) this.close();
      if (event.key === 'Tab' && this.isOpen) this.#trapFocus(event);
    });
  }

  get isOpen() { return this.panel.classList.contains('is-open'); }

  toggle() { this.isOpen ? this.close() : this.open(); }

  open() {
    this.lastFocus = document.activeElement;
    this.panel.classList.add('is-open');
    this.burger.setAttribute('aria-expanded', 'true');
    this.burger.setAttribute('aria-label', 'Fechar menu');
    document.body.style.overflow = 'hidden';
    this.panel.querySelector('a')?.focus({ preventScroll: true });
  }

  close() {
    this.panel.classList.remove('is-open');
    this.burger.setAttribute('aria-expanded', 'false');
    this.burger.setAttribute('aria-label', 'Abrir menu');
    document.body.style.overflow = '';
    this.lastFocus?.focus({ preventScroll: true });
  }

  #trapFocus(event) {
    const focusables = this.panel.querySelectorAll('a, button');
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (event.shiftKey && document.activeElement === first) { last.focus(); event.preventDefault(); }
    else if (!event.shiftKey && document.activeElement === last) { first.focus(); event.preventDefault(); }
  }
}
