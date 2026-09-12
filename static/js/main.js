/**
 * Orquestrador. Cada modulo tem uma responsabilidade e nao conhece os outros.
 * Se um modulo falhar, os demais continuam funcionando.
 */

import { Accordion } from './modules/accordion.js';
import { ContextCursor } from './modules/cursor.js';
import { DetailModal } from './modules/modal.js';
import { Header } from './modules/header.js';
import { HeroCanvas } from './modules/hero-canvas.js';
import { QuoteForm } from './modules/quote-form.js';
import { RevealObserver } from './modules/motion.js';
import { WhatsAppButton } from './modules/whatsapp.js';

const boot = (nome, fn) => {
  try { fn(); }
  catch (erro) { console.error(`[site] falha ao iniciar "${nome}"`, erro); }
};

document.addEventListener('DOMContentLoaded', () => {
  boot('header', () => new Header(document.querySelector('[data-header]')).init());
  boot('hero', () => {
    const canvas = document.querySelector('[data-hero-canvas]');
    if (canvas) new HeroCanvas(canvas).init();
  });
  boot('reveal', () => new RevealObserver().observe());
  boot('accordion', () => new Accordion(document.querySelector('[data-accordion]')).init());
  boot('modal', () => new DetailModal().init());
  boot('cursor', () => new ContextCursor(document.querySelector('[data-cursor]')).init());
  boot('form', () => new QuoteForm(document.querySelector('[data-quote-form]')).init());
  boot('whatsapp', () => new WhatsAppButton(document.querySelector('[data-wa]')).init());

  boot('ano', () => {
    const alvo = document.querySelector('[data-year]');
    if (alvo) alvo.textContent = new Date().getFullYear();
  });

  // CTA dentro do modal: fecha o modal antes de rolar ate o formulario.
  boot('modal-cta', () => {
    document.addEventListener('click', (evento) => {
      const gatilho = evento.target.closest('[data-modal-go]');
      if (!gatilho) return;
      document.querySelector('[data-modal-close]')?.click();
    });
  });
});
