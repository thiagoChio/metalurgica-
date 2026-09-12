/**
 * Modal unico para servicos e projetos.
 * Responsabilidades: montar o conteudo a partir do JSON embutido no HTML,
 * prender o foco enquanto aberto e devolver o foco ao fechar.
 */

const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
}[char]));

export class DetailModal {
  constructor() {
    this.root = document.querySelector('[data-modal]');
    this.body = document.querySelector('[data-modal-body]');
    this.services = this.#readJson('[data-services-json]');
    this.projects = this.#readJson('[data-projects-json]');
    this.lastFocus = null;
  }

  init() {
    if (!this.root) return;

    document.querySelectorAll('[data-service]').forEach((node) => {
      node.addEventListener('click', () => this.open(this.services[node.dataset.service]));
    });
    document.querySelectorAll('[data-project]').forEach((node) => {
      node.addEventListener('click', () => this.open(this.projects[node.dataset.project]));
    });
    document.querySelectorAll('[data-service-link]').forEach((node) => {
      node.addEventListener('click', (event) => {
        event.preventDefault();
        this.open(this.services[node.dataset.serviceLink]);
      });
    });

    this.root.querySelector('[data-modal-close]').addEventListener('click', () => this.close());
    this.root.addEventListener('click', (event) => { if (event.target === this.root) this.close(); });
    document.addEventListener('keydown', (event) => {
      if (!this.isOpen) return;
      if (event.key === 'Escape') this.close();
      if (event.key === 'Tab') this.#trapFocus(event);
    });
  }

  get isOpen() { return this.root.classList.contains('is-open'); }

  open(data) {
    if (!data) return;
    this.lastFocus = document.activeElement;
    this.body.innerHTML = data.kind === 'servico' ? this.#service(data) : this.#project(data);
    this.root.hidden = false;
    requestAnimationFrame(() => this.root.classList.add('is-open'));
    document.body.style.overflow = 'hidden';
    this.root.querySelector('[data-modal-close]').focus({ preventScroll: true });
  }

  close() {
    this.root.classList.remove('is-open');
    document.body.style.overflow = '';
    setTimeout(() => { this.root.hidden = true; this.body.innerHTML = ''; }, 380);
    this.lastFocus?.focus({ preventScroll: true });
  }

  // ------------------------------------------------------------- conteudo
  #service(data) {
    return `
      <p class="eyebrow">Serviço ${escapeHtml(data.number)}</p>
      <h2 id="modal-title">${escapeHtml(data.title)}</h2>
      <p style="color:var(--text-muted);font-size:var(--fs-lead);max-width:60ch">${escapeHtml(data.detail)}</p>
      <div class="modal__grid">
        ${this.#specList('Aplicações típicas', data.applications)}
        ${this.#specList('Materiais mais usados', data.materials)}
      </div>
      ${this.#actions(data.whatsapp, 'Pedir orçamento deste serviço')}`;
  }

  #project(data) {
    const aviso = data.is_placeholder
      ? `<p class="placeholder-note"><b>[ SUBSTITUIR ]</b> Desenho técnico gerado pelo site.
         Adicione as fotos reais deste projeto para publicar.</p>` : '';
    const imagens = data.gallery.map((src, index) => `
      <figure class="modal__figure">
        <img src="${escapeHtml(src)}" alt="${escapeHtml(data.title)} — imagem ${index + 1}"
             loading="lazy" decoding="async">
      </figure>`).join('');

    return `
      <p class="eyebrow">${escapeHtml(data.category)}</p>
      <h2 id="modal-title">${escapeHtml(data.title)}</h2>
      ${imagens}
      ${aviso}
      <p style="color:var(--text-muted);font-size:var(--fs-lead);max-width:60ch">${escapeHtml(data.summary)}</p>
      <div class="modal__grid">
        <dl class="spec"><dt>Finalidade</dt><dd>${escapeHtml(data.purpose)}</dd></dl>
        <dl class="spec"><dt>Local</dt><dd>${escapeHtml(data.location)}</dd></dl>
      </div>
      ${this.#specList('Materiais empregados', data.materials)}
      ${this.#actions(data.whatsapp, 'Quero algo parecido')}`;
  }

  #specList(title, items) {
    if (!items?.length) return '';
    return `
      <dl class="spec">
        <dt>${escapeHtml(title)}</dt>
        <dd><span class="tag-list">${items.map((i) => `<span class="tag">${escapeHtml(i)}</span>`).join('')}</span></dd>
      </dl>`;
  }

  #actions(whatsapp, label) {
    return `
      <div class="band" style="margin-top:var(--space-4)">
        <div class="band__text"><b>${escapeHtml(label)}</b>
          <span>Mande as medidas e uma foto do local — o retorno fica mais rápido.</span></div>
        <div class="band__actions">
          <a class="btn btn--sm" href="#orcamento" data-modal-go>
            <span class="btn__label">Solicitar orçamento</span></a>
          <a class="btn btn--ghost btn--sm" href="${escapeHtml(whatsapp)}" target="_blank" rel="noopener">
            <span class="btn__label">WhatsApp</span></a>
        </div>
      </div>`;
  }

  #trapFocus(event) {
    const focusables = this.root.querySelectorAll('a[href], button');
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (event.shiftKey && document.activeElement === first) { last.focus(); event.preventDefault(); }
    else if (!event.shiftKey && document.activeElement === last) { first.focus(); event.preventDefault(); }
  }

  #readJson(selector) {
    try { return JSON.parse(document.querySelector(selector)?.textContent || '{}'); }
    catch { return {}; }
  }
}
