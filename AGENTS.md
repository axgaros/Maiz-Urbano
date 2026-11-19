# Instrucciones permanentes para asistentes — Maíz Urbano

**Leer obligatoriamente antes de modificar cualquier archivo de UI:**
1. `README.md`
2. `DESIGN.md` (fuente de verdad visual)
3. `UX-FLOWS.md`
4. Este archivo

## Skills de consulta obligatoria

En cada tarea de diseño o frontend, usar las metodologías de estas cinco referencias:
- Anthropic Frontend Design: https://github.com/anthropics/skills/tree/main/skills/frontend-design
- UI UX Pro Max: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Impeccable: https://github.com/pbakaus/impeccable
- Vercel Web Design Guidelines: https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines
- OpenAI Playwright: https://github.com/openai/skills/tree/main/skills/.curated/playwright

**Estas son referencias externas, no paquetes instalados.** Cuando haya acceso a la skill original, leerla y aplicar sus reglas compatibles con el proyecto; no decir que se ejecutó una herramienta si no se ejecutó. Para Vercel, consultar su guía vigente antes de cada auditoría. Para Playwright, realizar pruebas de navegador y capturas cuando el entorno lo permita.

## Pautas no negociables

- Mantener identidad Street Food Editorial aprobada.
- **Imágenes únicamente en la pantalla de registro de Ventas**, nunca en otros módulos.
- Código vanilla HTML/CSS/JS, Python + pywebview + SQLite, ejecución offline.
- No introducir React, Tailwind, Electron, CDN, hosting ni cuentas sin autorización.
- No fabricar costos por receta, consumos de elote por porción, gramajes, utilidades ni resultados reales.
- Reportes son tablas internas con historial persistente, no descargas Excel obligatorias.
- Toda afirmación de “guardado” exige confirmación real de SQLite.
- HTML semántico, etiquetas visibles, foco de teclado y mensajes de error accesibles.
- No implementar botones sin acción ni rutas ficticias como si fueran reales.
- Documentar lo que efectivamente funciona y lo que sigue pendiente.
- Al trabajar frontend: revisar con heurísticas de diseño, guía Vercel, pruebas Playwright y contraste.
- Cualquier cambio a decisiones aprobadas requiere explicación y autorización del usuario.

## Protocolo de cada cambio

1. Leer documentos y referencias de skills relevantes.
2. Escribir plan de una frase y aceptación verificable.
3. Modificar solo el alcance de la tarea.
4. Probar sintaxis, lógica y funcionamiento; capturas si hay navegador.
5. Auditar diseño, usabilidad, accesibilidad, estados y operaciones offline.
6. Registrar limitaciones verificadas y actualizar documentación si cambia el alcance.
7. Publicar cambios con commits descriptivos; no afirmar pruebas no ejecutadas.

Consultar `QA-UI.md` para revisiones por pantalla.
