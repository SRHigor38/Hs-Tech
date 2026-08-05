/**
 * HS Tech — Animações
 * Scroll reveal com IntersectionObserver + filtro de projetos.
 */

export function initAnimations() {
    initScrollReveal();
    initProjectFilters();
}

/**
 * Scroll Reveal — elementos com classe .reveal aparecem suavemente
 * ao entrar na viewport. Respeita prefers-reduced-motion.
 */
function initScrollReveal() {
    const elements = document.querySelectorAll('.reveal');
    if (!elements.length) return;

    // Se o usuário prefere menos movimento, mostra tudo imediatamente
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        elements.forEach((el) => el.classList.add('reveal--visivel'));
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('reveal--visivel');
                    observer.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px',
        }
    );

    elements.forEach((el) => observer.observe(el));
}

/**
 * Filtro de projetos — filtra os cards por categoria.
 */
function initProjectFilters() {
    const filters = document.querySelectorAll('.filtro');
    const cards = document.querySelectorAll('.card--projeto');
    if (!filters.length || !cards.length) return;

    filters.forEach((filter) => {
        filter.addEventListener('click', () => {
            // Atualiza o botão ativo
            filters.forEach((f) => f.classList.remove('filtro--ativo'));
            filter.classList.add('filtro--ativo');

            const categoria = filter.dataset.filtro;

            cards.forEach((card) => {
                const cardCategoria = card.dataset.categoria;
                const shouldShow = categoria === 'Todos' || cardCategoria === categoria;

                card.style.display = shouldShow ? '' : 'none';

                // Re-anima o card ao aparecer
                if (shouldShow) {
                    card.classList.remove('reveal--visivel');
                    requestAnimationFrame(() => {
                        requestAnimationFrame(() => {
                            card.classList.add('reveal--visivel');
                        });
                    });
                }
            });
        });
    });
}