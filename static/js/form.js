/**
 * HS Tech — Formulário de Contato
 * Validação em tempo real, máscara de telefone e envio via WhatsApp.
 */

export function initForm() {
    const form = document.getElementById('contatoForm');
    if (!form) return;

    const fields = {
        nome: form.querySelector('#nome'),
        email: form.querySelector('#email'),
        telefone: form.querySelector('#telefone'),
        assunto: form.querySelector('#assunto'),
        mensagem: form.querySelector('#mensagem'),
    };

    const submitBtn = form.querySelector('#submitBtn');
    const alertSucesso = form.querySelector('#alertSucesso');
    const alertErro = form.querySelector('#alertErro');

    // Máscara de telefone: (38) 99138-8394
    const applyPhoneMask = (value) => {
        const digits = value.replace(/\D/g, '').slice(0, 11);
        if (digits.length <= 2) return digits;
        if (digits.length <= 6) return `(${digits.slice(0, 2)}) ${digits.slice(2)}`;
        if (digits.length <= 10) {
            return `(${digits.slice(0, 2)}) ${digits.slice(2, 6)}-${digits.slice(6)}`;
        }
        return `(${digits.slice(0, 2)}) ${digits.slice(2, 7)}-${digits.slice(7)}`;
    };

    // Validações
    const validators = {
        nome: (value) => value.trim().length >= 3,
        email: (value) => /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value.trim()),
        telefone: (value) => value.replace(/\D/g, '').length >= 10,
        assunto: (value) => value.trim().length > 0,
        mensagem: (value) => value.trim().length >= 10,
    };

    const errorMessages = {
        nome: 'Digite seu nome completo (mínimo 3 letras).',
        email: 'Digite um e-mail válido.',
        telefone: 'Digite um telefone válido com DDD.',
        assunto: 'Selecione um assunto.',
        mensagem: 'Digite uma mensagem com pelo menos 10 caracteres.',
    };

    // Valida um campo individual
    const validateField = (field) => {
        const name = field.id;
        const value = field.value;
        const isValid = validators[name](value);
        const errorEl = form.querySelector(`#${name}Error`);

        field.classList.toggle('form-input--erro', !isValid && value.length > 0);
        field.classList.toggle('form-input--sucesso', isValid);

        if (errorEl) {
            errorEl.textContent = errorMessages[name];
            errorEl.classList.toggle('form-error--visivel', !isValid && value.length > 0);
        }

        return isValid;
    };

    // Valida todos os campos
    const validateAll = () => {
        let allValid = true;
        Object.values(fields).forEach((field) => {
            if (field && !validateField(field)) {
                allValid = false;
            }
        });
        return allValid;
    };

    // Eventos de validação em tempo real
    Object.values(fields).forEach((field) => {
        if (!field) return;

        field.addEventListener('blur', () => validateField(field));
        field.addEventListener('input', () => {
            if (field.id === 'telefone') {
                field.value = applyPhoneMask(field.value);
            }
            if (field.classList.contains('form-input--erro')) {
                validateField(field);
            }
        });
    });

    // Envio do formulário
    form.addEventListener('submit', (event) => {
        event.preventDefault();

        // Esconde alertas anteriores
        alertSucesso?.classList.remove('alert--visivel');
        alertErro?.classList.remove('alert--visivel');

        // Valida tudo
        if (!validateAll()) {
            alertErro?.classList.add('alert--visivel');
            return;
        }

        // Estado de loading
        submitBtn.classList.add('btn--loading');
        submitBtn.disabled = true;

        // Monta a mensagem do WhatsApp
        const mensagem = [
            'Olá! Visitei o site da HS Tech e gostaria de solicitar um orçamento.',
            '',
            `*Nome:* ${fields.nome.value.trim()}`,
            `*E-mail:* ${fields.email.value.trim()}`,
            `*Telefone:* ${fields.telefone.value.trim()}`,
            `*Assunto:* ${fields.assunto.value}`,
            '',
            `*Mensagem:*`,
            fields.mensagem.value.trim(),
        ].join('\n');

        // Abre o WhatsApp com a mensagem
        const whatsappNumber = document.body.dataset.whatsapp || '5538991388394';
        const url = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(mensagem)}`;

        // Simula um pequeno delay para feedback visual
        setTimeout(() => {
            submitBtn.classList.remove('btn--loading');
            submitBtn.disabled = false;

            // Mostra sucesso
            alertSucesso?.classList.add('alert--visivel');

            // Abre o WhatsApp
            window.open(url, '_blank', 'noopener');

            // Limpa o formulário
            form.reset();
            Object.values(fields).forEach((field) => {
                if (field) {
                    field.classList.remove('form-input--sucesso', 'form-input--erro');
                }
            });

            // Esconde o alerta de sucesso após 5 segundos
            setTimeout(() => {
                alertSucesso?.classList.remove('alert--visivel');
            }, 5000);
        }, 800);
    });
}