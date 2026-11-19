# Checklist de publicação

Publicação e alterações de infraestrutura exigem autorização explícita.

- [ ] Aprovar domínio, hospedagem e escopo.
- [ ] Revisar segurança e dependências, e instalar em ambiente limpo.
- [ ] Configurar segredo, banco persistente e Redis real; testar limites compartilhados com processos reais. A simulação local não substitui este teste.
- [ ] Trocar senha inicial; testar autorização, CSRF, sessão e rate limiting entre processos.
- [ ] Revisar migrações em cópia; testar backup e restauração do banco e arquivos.
- [ ] Configurar HTTPS, proxy confiável, armazenamento persistente, logs e alertas; proteger logs do servidor e proxy contra dados pessoais.
- [ ] Aprovar política de privacidade e proposta de retenção, incluindo tratamento de backups e direitos dos titulares.
- [ ] Testar páginas, acessibilidade, funcionamento móvel e recuperação de falhas.
- [ ] Manter demonstrações em rascunho até auditoria, isolamento real e autorização.
- [ ] Obter autorização específica antes do deploy.

## Itens específicos para Render

- [ ] Aprovar custos, provedor PostgreSQL, Redis e sua política de backup.
- [ ] Testar migrações e CRUD em PostgreSQL real descartável; ensaiar recuperação.
- [ ] Validar Redis real, limitação por IP e cabeçalhos da borda Render.
- [ ] Verificar disco de imagens após restart e restaurar cópia em ambiente separado.
- [ ] Adicionar capturas reais anonimizadas aos três projetos; manter demos interativas isoladas.
- [ ] Criar administrador de produção por prompt, sem senha de desenvolvimento.
- [ ] Confirmar HTTPS, CSRF, autenticação, uploads, limites e monitoramento no ambiente autorizado.
- [ ] Obter autorização antes de criar recursos, sincronizar Blueprint ou publicar.
