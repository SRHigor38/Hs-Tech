document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('[data-quote-form]');
  if (!form) return;
  form.addEventListener('submit', () => {
    if (!form.checkValidity()) return;
    const button = form.querySelector('button[type="submit"]');
    if (button.disabled) return;
    button.disabled = true;
    button.querySelector('span').textContent = 'Enviando solicitação…';
    button.setAttribute('aria-busy', 'true');
  });
});

window.addEventListener('pageshow', () => {
  const button = document.querySelector('[data-quote-form] button[type="submit"]');
  if (!button) return;
  button.disabled = false;
  button.removeAttribute('aria-busy');
  button.querySelector('span').textContent = 'Enviar minha solicitação';
});
