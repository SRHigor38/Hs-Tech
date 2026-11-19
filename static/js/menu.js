/**
 * HS Tech — Menu de navegação
 * Controla o menu mobile (hamburger), navbar com scroll e fechamento ao clicar fora.
 */

export function initMenu() {
    const navbar = document.getElementById('navbar');
    const toggle = document.getElementById('navbarToggle');
    const nav = document.getElementById('navbarNav');

    if (!navbar || !toggle || !nav) return;

    // Navbar com sombra ao rolar
    const handleScroll = () => {
        navbar.classList.toggle('navbar--scrolled', window.scrollY > 50);
    };

    // Abrir/fechar menu mobile
    const toggleMenu = () => {
        const isOpen = nav.classList.toggle('navbar__nav--aberto');
        toggle.classList.toggle('navbar__hamburger--ativo', isOpen);
        toggle.setAttribute('aria-expanded', String(isOpen));
        toggle.setAttribute('aria-label', isOpen ? 'Fechar menu' : 'Abrir menu');
        document.body.style.overflow = isOpen ? 'hidden' : '';
        if (isOpen) nav.querySelector('a')?.focus();
    };

    // Fechar menu ao clicar em um link
    const closeMenu = () => {
        nav.classList.remove('navbar__nav--aberto');
        toggle.classList.remove('navbar__hamburger--ativo');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Abrir menu');
        document.body.style.overflow = '';
    };

    // Fechar menu ao clicar fora
    const handleClickOutside = (event) => {
        if (nav.classList.contains('navbar__nav--aberto') &&
            !nav.contains(event.target) &&
            !toggle.contains(event.target)) {
            closeMenu();
        }
    };

    // Fechar menu com tecla ESC
    const handleEscape = (event) => {
        if (event.key === 'Escape' && nav.classList.contains('navbar__nav--aberto')) {
            closeMenu();
            toggle.focus();
        }
    };

    toggle.addEventListener('click', toggleMenu);
    nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
    document.addEventListener('click', handleClickOutside);
    document.addEventListener('keydown', handleEscape);
    window.addEventListener('scroll', handleScroll, { passive: true });

    // Estado inicial
    handleScroll();
}