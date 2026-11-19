# Maíz Urbano — lista de revisión UX/UI

Inspirado en Frontend Design, UI UX Pro Max, Impeccable, Vercel Web Design Guidelines y Playwright; no sustituye la ejecución de dichas herramientas.

## Comprobaciones

- [ ] Nombre y jerarquía de cada pantalla claros; solo una acción principal visible.
- [ ] Seis apartados navegables; el actual se distingue sin depender solo de color.
- [ ] Imágenes solo en Ventas; iconos operativos sin emoji.
- [ ] Productos con nombre completo, variante y precio visible.
- [ ] Botones reales; teclado/tabulación/Enter; foco visible.
- [ ] Formularios con label, campos requeridos, errores junto al campo.
- [ ] Las tablas tienen `th`, encabezados y estado vacío.
- [ ] Toast o estado con `aria-live` y éxito posterior a guardar realmente.
- [ ] No hay `transition: all`, animaciones innecesarias o motion obligatorio.
- [ ] Contraste WCAG 2.2 AA; se respeta `prefers-reduced-motion`.
- [ ] El diseño funciona en 1280×720 y 1366×768, sin contenido esencial cortado.
- [ ] El sistema funciona offline (sin recursos externos en runtime).
- [ ] SQLite conserva registros al cerrar/reabrir.
- [ ] Reportes guardados accesibles desde historial y reversibles con “Volver a reportes”.
- [ ] Los datos ficticios están etiquetados y no hay costos inventados.
- [ ] Se registra evidencia de pruebas; casillas no marcadas no implican incumplimiento.

## Revisiones técnicas recomendadas

- Validar HTML, CSS y JavaScript.
- Auditar guía Vercel con referencias exactas a archivo:línea.
- Revisión crítica de patrones genéricos con Impeccable.
- Playwright: navegar, registrar venta, visitar inventario, consultar reporte, capturar a tamaños de escritorio.
- Verificar versión final real en pywebview Windows con archivos offline.
