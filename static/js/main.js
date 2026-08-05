/**
 * HS Tech — Ponto de entrada JavaScript
 * Importa e inicializa todos os módulos da aplicação.
 */

import { initMenu } from './menu.js';
import { initAnimations } from './animations.js';
import { initForm } from './form.js';

document.addEventListener('DOMContentLoaded', () => {
    initMenu();
    initAnimations();
    initForm();
});