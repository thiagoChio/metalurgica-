/**
 * Formulario de orcamento em tres etapas (progressive disclosure).
 *
 * A validacao aqui e ESPELHO da validacao do servidor (app/models/schemas.py),
 * nunca substituta: serve para dar erro imediato e específico, no campo certo.
 */

const MESSAGES = {
  service: 'Escolha o tipo de serviço para continuarmos.',
  description: 'Conte em algumas linhas o que você precisa.',
  name: 'Informe seu nome para sabermos com quem falamos.',
  whatsapp: 'Informe seu WhatsApp para continuarmos.',
  city: 'Informe a cidade onde o serviço será executado.',
};

const MAX_BYTES = 10 * 1024 * 1024;

export class QuoteForm {
  constructor(form) {
    this.form = form;
    this.stage = 0;
    this.files = [];
  }

  init() {
    if (!this.form) return;
    this.stages = [...this.form.querySelectorAll('[data-stage]')];
    this.progress = this.form.querySelector('[data-form-progress]');
    this.steps = [...document.querySelectorAll('[data-step-index]')];
    this.prev = this.form.querySelector('[data-prev]');
    this.next = this.form.querySelector('[data-next]');
    this.submit = this.form.querySelector('[data-submit]');
    this.nav = this.form.querySelector('[data-form-nav]');
    this.result = this.form.querySelector('[data-form-result]');

    this.prev.addEventListener('click', () => this.go(this.stage - 1));
    this.next.addEventListener('click', () => this.#advance());
    this.form.addEventListener('submit', (event) => this.#send(event));

    // Escolher o servico avanca sozinho: menos um clique na etapa mais facil.
    this.form.querySelectorAll('[data-service-choice]').forEach((input) => {
      input.addEventListener('change', () => {
        this.#clearError('service');
        setTimeout(() => this.#advance(), 220);
      });
    });

    this.form.querySelectorAll('.field__control').forEach((control) => {
      control.addEventListener('input', () => this.#clearError(control.name));
    });

    this.#mask();
    this.#dropzone();
    this.#render();
  }

  // ------------------------------------------------------------- navegacao
  go(index) {
    this.stage = Math.max(0, Math.min(index, this.stages.length - 1));
    this.#render();
    this.form.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  #advance() {
    if (!this.#validate(this.stage)) return;
    if (this.stage === this.stages.length - 1) return;
    this.go(this.stage + 1);
  }

  #render() {
    this.stages.forEach((stage, index) => stage.classList.toggle('is-active', index === this.stage));
    this.steps.forEach((step, index) => {
      step.classList.toggle('is-current', index === this.stage);
      step.classList.toggle('is-done', index < this.stage);
    });
    this.progress.style.width = `${((this.stage + 1) / this.stages.length) * 100}%`;
    this.prev.hidden = this.stage === 0;
    const ultima = this.stage === this.stages.length - 1;
    this.next.hidden = ultima;
    this.submit.hidden = !ultima;
  }

  // ------------------------------------------------------------- validacao
  #validate(stage) {
    const regras = [
      () => (this.form.querySelector('[name="service"]:checked') ? null : ['service', MESSAGES.service]),
      () => {
        const texto = this.form.elements.description.value.trim();
        return texto.length >= 10 ? null : ['description', MESSAGES.description];
      },
      () => {
        const nome = this.form.elements.name.value.trim();
        if (nome.length < 2) return ['name', MESSAGES.name];
        const digitos = this.form.elements.whatsapp.value.replace(/\D/g, '');
        if (digitos.length < 10) return ['whatsapp', 'Informe o WhatsApp com DDD, ex.: (65) 99999-9999.'];
        if (this.form.elements.city.value.trim().length < 2) return ['city', MESSAGES.city];
        return null;
      },
    ];

    const falha = regras[stage]?.();
    if (!falha) return true;
    this.#showError(falha[0], falha[1]);
    return false;
  }

  #showError(field, message) {
    const wrapper = this.form.querySelector(`[data-field="${field}"]`);
    const slot = this.form.querySelector(`[data-error="${field}"]`);
    if (slot) slot.textContent = message;
    wrapper?.classList.add('has-error');
    const control = this.form.elements[field];
    if (control?.focus) control.focus({ preventScroll: true });
    (wrapper || slot)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  #clearError(field) {
    if (!field) return;
    this.form.querySelector(`[data-field="${field}"]`)?.classList.remove('has-error');
    const slot = this.form.querySelector(`[data-error="${field}"]`);
    if (slot) slot.textContent = '';
  }

  // ------------------------------------------------------------- utilidades
  #mask() {
    const campo = this.form.querySelector('[data-phone-mask]');
    if (!campo) return;
    campo.addEventListener('input', () => {
      const d = campo.value.replace(/\D/g, '').slice(0, 11);
      campo.value = d.length <= 2 ? d
        : d.length <= 6 ? `(${d.slice(0, 2)}) ${d.slice(2)}`
        : d.length <= 10 ? `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`
        : `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}`;
    });
  }

  #dropzone() {
    const zona = this.form.querySelector('[data-dropzone]');
    const input = this.form.querySelector('[data-file-input]');
    const lista = this.form.querySelector('[data-file-list]');
    if (!zona || !input) return;

    const desenhar = () => {
      lista.innerHTML = this.files.map((file, index) => `
        <div class="file-chip">
          <span>${file.name} — ${(file.size / 1024 / 1024).toFixed(1)} MB</span>
          <button type="button" data-remove="${index}" aria-label="Remover ${file.name}">remover</button>
        </div>`).join('');
      lista.querySelectorAll('[data-remove]').forEach((botao) => {
        botao.addEventListener('click', () => {
          this.files.splice(Number(botao.dataset.remove), 1);
          desenhar();
        });
      });
    };

    const adicionar = (novos) => {
      [...novos].forEach((file) => {
        if (file.size > MAX_BYTES) {
          this.#showError('geral', `"${file.name}" passa de 10 MB. Reduza o arquivo e tente de novo.`);
          return;
        }
        this.files.push(file);
      });
      desenhar();
    };

    input.addEventListener('change', () => adicionar(input.files));
    ['dragenter', 'dragover'].forEach((evt) => zona.addEventListener(evt, (e) => {
      e.preventDefault(); zona.classList.add('is-dragging');
    }));
    ['dragleave', 'drop'].forEach((evt) => zona.addEventListener(evt, (e) => {
      e.preventDefault(); zona.classList.remove('is-dragging');
    }));
    zona.addEventListener('drop', (e) => adicionar(e.dataTransfer.files));
  }

  // ------------------------------------------------------------------ envio
  async #send(event) {
    event.preventDefault();
    if (!this.#validate(2)) return;

    this.submit.classList.add('btn--loading');
    this.submit.disabled = true;
    this.#clearError('geral');

    const dados = new FormData();
    ['service', 'description', 'measurements', 'deadline', 'name', 'whatsapp', 'city']
      .forEach((campo) => {
        const elemento = this.form.elements[campo];
        dados.append(campo, elemento?.value ?? '');
      });
    dados.set('service', this.form.querySelector('[name="service"]:checked')?.value ?? '');
    this.files.forEach((file) => dados.append('files', file));

    try {
      const resposta = await fetch(this.form.action, { method: 'POST', body: dados });
      const corpo = await resposta.json();

      if (!resposta.ok) {
        Object.entries(corpo.errors || {}).forEach(([campo, mensagem], index) => {
          if (index === 0) this.#showError(campo, mensagem);
          else {
            const slot = this.form.querySelector(`[data-error="${campo}"]`);
            if (slot) slot.textContent = mensagem;
            this.form.querySelector(`[data-field="${campo}"]`)?.classList.add('has-error');
          }
        });
        return;
      }

      this.stages.forEach((stage) => stage.classList.remove('is-active'));
      this.nav.hidden = true;
      this.result.classList.add('is-active');
      this.progress.style.width = '100%';
      this.form.querySelector('[data-protocol]').textContent = `Protocolo ${corpo.protocol}`;
      this.steps.forEach((step) => step.classList.add('is-done'));
    } catch {
      this.#showError('geral',
        'Não conseguimos enviar agora. Verifique sua conexão ou fale direto pelo WhatsApp.');
    } finally {
      this.submit.classList.remove('btn--loading');
      this.submit.disabled = false;
    }
  }
}
