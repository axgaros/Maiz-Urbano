# Maíz Urbano — Sistema de diseño

**Estado:** dirección artística aprobada · 19 de noviembre de 2026.  
**Proyecto:** aplicación local de escritorio para una demostración académica.

## Identidad

**Street Food Editorial**. Gráfica enérgica, urbana y distintiva de Maíz Urbano; área de trabajo sobria y legible. No transformar el negocio en un SaaS corporativo genérico. El recurso hero de marca inspira, pero no se copia como fondo de la interfaz de trabajo.

### Paleta

| Token | Color | Uso |
|---|---|---|
| `--maiz` | `#FFCA05` | Acción principal, selección y acentos |
| `--ink` | `#101010` | Sidebar y tipografía principal |
| `--red` | `#D91F26` | Acento de marca controlado; errores con texto |
| `--cream` | `#FFF9EF` | Superficie de trabajo |
| `--line` | `#E6E2D9` | Divisores y contornos |
| `--paper` | `#FFFFFF` | Formularios y tablas |
| `--muted` | `#605B52` | Texto secundario con contraste verificado |

El rojo de marca **no** debe implicar error si no corresponde. Nunca depender solo de color para comunicar un estado.

## Tipografía

- Display: **Arial Black / Arial** hasta integrar una fuente licenciada, local y aprobada. No cargar Google Fonts ni CDN.
- Interfaz: **Segoe UI / Arial**, fuentes locales de Windows, por legibilidad.
- Jerarquía: título 32–36px; subtítulo 20–24px; texto 14–16px; etiquetas 12–13px. Texto de tabla >= 13px.
- Cifras de dinero: `font-variant-numeric: tabular-nums`; moneda `es-MX` con `Intl.NumberFormat`.
- Textos de acciones con verbos claros: “Registrar venta”, “Guardar entrada”, “Volver a reportes”.

## Layout

- Navegación lateral permanente de 230–250px; contenido flexible.
- Secciones principales: **Inicio, Ventas, Inventario, Compras y gastos, Caja, Reportes**.
- Cada sección tiene encabezado propio, acciones primarias y estado vacío.
- **Imágenes exclusivamente en las tarjetas de productos de Ventas**. No mostrar fotografías, ilustraciones ni adornos en Inicio, Inventario, Compras, Caja o Reportes. Iconos funcionales de línea son aceptables.
- Tarjetas para selección de productos; tablas y superficies limpias para datos. Evitar encerrar todos los elementos en tarjetas innecesarias.
- Bordes redondeados moderados (8–16px); sombras sutiles o ninguna; sin glassmorphism, degradados decorativos ni animaciones de entrada arbitrarias.
- Usar espacio para jerarquía; no para decorar.

## Comportamiento de interfaz

- Vistas dentro de una única ventana (no navegación a páginas web remotas).
- Sidebar: selección persistente; cualquier apartado accesible en un clic.
- Ventas: tarjetas visuales con nombre, variante, precio, imagen y botón de agregar. Carrito con cantidad, eliminación, total y método de cobro.
- Inventario: pestañas Existencias, Entradas, Caducidades, Mermas; formularios asociados.
- Reportes: historial por semanas; cada reporte guardado se abre en detalle con tablas; “Volver a reportes” no cierra la app.
- Confirmación antes de pérdida de datos; sin mensajes de éxito falsos.
- Fechas, moneda, encabezados de tablas y vacíos claros.
- Al acceder con teclado: foco visible, etiquetas semánticas, orden lógico y área interactiva confortable.
- `prefers-reduced-motion` reduce efectos; transiciones solo de color/transform/opacity cuando comunican estado.

## Qué evita el resultado genérico

1. **La marca manda**: identidad cromática e industria del elote, sin plantilla SaaS universal.
2. **Una acción central por vista**: nada de nueve gráficas de relleno.
3. **Fotografía/ilustración restringida a Ventas**, para ayudar a reconocer productos.
4. **Los datos importan más que los adornos**: reportes como tablas, no gráficos solo para impresionar.
5. **Sistemas coherentes**: mismos botones, inputs, unidades, espaciados y estados.
6. **Contenido veraz**: datos simulados etiquetados; nunca inventar ventas reales, costos o cantidades.

## Skills y referencias obligatorias para cada iteración UI

**Consultar sus versiones originales al comenzar una tarea de interfaz** (las skills externas NO se han instalado ni copiado en este repositorio):

1. [Anthropic Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design): plan intencional y autocrítica de estilo.
2. [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill): diseño de sistema, navegación, accesibilidad, tipografía y criterios verificables.
3. [Impeccable](https://github.com/pbakaus/impeccable): crítica del diseño y detección de patrones genéricos.
4. [Vercel Web Design Guidelines](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines): auditoría de HTML, foco, formularios, tablas y semántica.
5. [OpenAI Playwright](https://github.com/openai/skills/tree/main/skills/.curated/playwright): inspección de navegador, capturas y pruebas reales.

Protocolo: leer **README.md → DESIGN.md → UX-FLOWS.md → AGENTS.md**; planear; implementar; revisar visualmente; auditar accesibilidad; probar. Si no están disponibles skills externas o navegador, decirlo: no afirmar auditoría que no se ejecutó.

### Criterios de aceptación

- Funciona offline, sin solicitudes de red.
- Contrastes conforme a WCAG 2.2 AA donde aplique.
- Controles utilizables con teclado; errores anunciados y corregibles.
- Imágenes de productos solamente en Ventas.
- Persistencia real en SQLite para registros que se señalan como guardados.
- No inventa costos por receta ni utilidades.
- Contenido usable a 1280×720 y a 1366×768 en Windows.
- Sin dependencias externas en tiempo de ejecución.
