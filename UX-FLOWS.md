# Maíz Urbano — Navegación y flujos UX

**Estado:** primera implementación en desarrollo; flujo definido en noviembre de 2026.

## Navegación

```text
Aplicación
├─ Inicio — resumen de actividad e instrucciones
├─ Ventas — catálogo visual, venta actual, historial
├─ Inventario — Existencias / Entradas / Caducidades / Mermas
├─ Compras y gastos — registrar y consultar movimientos
├─ Caja — iniciar jornada / registrar movimientos / cerrar
└─ Reportes — historial semanal → detalle guardado → volver
```

## Flujo de ventas

1. Abrir **Ventas**. Solo aquí se utilizan imágenes de productos.
2. Seleccionar producto/variante mediante tarjeta clara; añadir al carrito.
3. Ajustar cantidades, revisar total y seleccionar método de cobro.
4. Pulsar **Registrar venta**. Guardar mediante Python/SQLite con transacción.
5. Confirmar **solo después** de que SQLite reporte éxito; vaciar carrito y actualizar datos.

Se preservan nombres y precios de menú proporcionado; no se infieren gramajes.

## Inventario

1. Abrir **Inventario** y consultar existencias.
2. Registrar una entrada con cantidad, unidad, fecha de compra y fecha de caducidad opcional.
3. Registrar merma/ajuste manual, justificando el cambio.
4. Mostrar alertas de fecha por ingreso, no un supuesto vencimiento general del ingrediente.

Las ventas de preparaciones NO consumen automáticamente ingredientes de proporciones desconocidas. Unidades empaquetadas solo se descuentan si su relación 1:1 está definida y verificada en implementación.

## Reportes

1. Abrir **Reportes** y consultar historial guardado.
2. **Generar reporte semanal** crea fotografía persistente de un periodo (lunes a domingo) con datos del momento.
3. Seleccionar reporte guardado; visualizar tablas: ventas por día, artículos vendidos, compras y gastos.
4. **Volver a reportes** regresa al historial dentro de la misma ventana.
5. Reportes anteriores no se reescriben al cambiar operaciones; generar uno nuevo para actualizar.
6. No hay exportación Excel como experiencia principal, por decisión posterior del usuario.

## Estados indispensables

- Estado vacío explicativo y acción próxima.
- Error con explicación útil, sin borrar datos ingresados.
- Confirmación visual al guardar con éxito.
- Carga o bloqueo temporal al guardar para evitar doble envío.
- Cierre de aplicación conserva SQLite en `data/`.

## Límites de la demostración

Un solo usuario, Windows, offline, sin hosting/autenticación/sincronización y sin costeo por receta. Datos de ejemplo identificados como ficticios.
