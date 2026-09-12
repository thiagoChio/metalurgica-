/**
 * Botao flutuante do WhatsApp.
 * Aparece depois do hero (antes disso ele competiria com o CTA principal) e
 * troca a mensagem pre-preenchida conforme o servico que o visitante escolheu.
 */

export class WhatsAppButton {
  constructor(node) { this.node = node; }

  init() {
    if (!this.node) return;

    const avaliar = () => {
      const passouDoHero = window.scrollY > window.innerHeight * 0.55;
      this.node.classList.toggle('is-visible', passouDoHero);
    };
    avaliar();
    window.addEventListener('scroll', avaliar, { passive: true });

    // Contexto: o servico escolhido no formulario muda a mensagem do botao.
    const servicos = this.#payload();
    document.querySelectorAll('[data-service-choice]').forEach((input) => {
      input.addEventListener('change', () => {
        const alvo = servicos[input.value];
        if (alvo?.whatsapp) this.node.href = alvo.whatsapp;
      });
    });

    // Abrir um servico tambem contextualiza o botao.
    document.querySelectorAll('[data-service]').forEach((node) => {
      node.addEventListener('click', () => {
        const alvo = servicos[node.dataset.service];
        if (alvo?.whatsapp) this.node.href = alvo.whatsapp;
      });
    });
  }

  #payload() {
    try { return JSON.parse(document.querySelector('[data-services-json]')?.textContent || '{}'); }
    catch { return {}; }
  }
}
