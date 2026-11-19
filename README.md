# Maíz Urbano — Sistema local de gestión

> **Estado:** primera versión de código publicada; integración pywebview y empaquetado `.exe` pendientes de validar en Windows.  
> **Tipo:** proyecto académico para una clase de economía, con prototipo funcional de escritorio.  
> **Fecha de definición:** 19 de noviembre de 2026.  
> **Entorno de demostración:** una sola computadora Windows, sin internet ni hosting.

## 0. Primera implementación disponible

**19 de noviembre de 2026:** se publicó código para seis apartados (Inicio, Ventas, Inventario, Compras y gastos, Caja y Reportes), una base SQLite local y pruebas de Python. Se verificaron seis pruebas automatizadas y las pantallas en Chromium. Todavía no se ha probado la ventana pywebview ni el `.exe` en Windows.

**Abrir en Windows:** instalar Python, ejecutar `py -m pip install -r requirements.txt` y después `py main.py` dentro de la carpeta del proyecto. La instalación de dependencias puede requerir internet inicialmente; el uso posterior se diseñó offline.

**Construir ejecutable portable:** ejecutar `powershell -ExecutionPolicy Bypass -File .\build_windows.ps1` en Windows. Mantener la carpeta de salida completa; validar WebView2 y la compilación antes de una exposición.

**Guías obligatorias de interfaz:** [DESIGN.md](DESIGN.md), [UX-FLOWS.md](UX-FLOWS.md), [AGENTS.md](AGENTS.md), [QA-UI.md](QA-UI.md). Las cinco skills de referencia están enlazadas, pero no se instalaron automáticamente.

## 1. Contexto del negocio

**Maíz Urbano** es una microempresa de elotes y antojitos en Guadalajara, Jalisco, México. La atiende una sola persona. Su horario aproximado de venta es de **18:00 a 22:00** y se abastece principalmente en el **Mercado de Abastos**. La ubicación de referencia proporcionada es **Isla Cozumel 3018**, próxima al cruce con López de Legazpi; el domicilio exacto no se ha verificado.

El proyecto no pretende entregar todavía una plataforma al propietario: **el estudiante la utilizará exclusivamente en su computadora para exhibir el funcionamiento en clase**.

### Menú de referencia

Los siguientes precios provienen del menú visual proporcionado; no se deben inferir costos de producción a partir de ellos.

| Producto o variante | Precio de venta (MXN) |
| --- | ---: |
| Desgranado grande con crema, mayonesa y queso | $55 |
| Desgranado mediano con crema, mayonesa y queso | $45 |
| Desgranado chico con crema, mayonesa y queso | $40 |
| Desgranado grande con sal, limón y chile | $50 |
| Desgranado mediano con sal, limón y chile | $35 |
| Desgranado chico con sal, limón y chile | $30 |
| Elote entero con crema, mayonesa y queso | $35 |
| Elote entero con sal, limón y chile | $25 |
| Tostielote | $70 |
| Papalote | $50 |
| Maruchan con elote | $85 |

Se han mencionado bebidas Boing, pero **no se ha confirmado su catálogo ni precio**. El material gráfico de marca y las fotografías del menú se compartieron como referencia, pero todavía no se han integrado al repositorio.

## 2. Objetivo y alcance aprobado

Construir una aplicación de escritorio pequeña, comprensible y operativa para demostrar seis procesos:

1. **Ventas:** registrar productos, cantidades, precios vigentes, método de cobro, fecha y hora; consultar y corregir operaciones mediante registros trazables.
2. **Compras y gastos:** capturar cantidades, fechas, conceptos y montos cuando se conozcan, sin inventar información.
3. **Inventario:** controlar existencias de ingredientes, alimentos empaquetados, bebidas y desechables mediante entradas, salidas y ajustes.
4. **Caducidades y mermas:** identificar cada ingreso por separado, registrar fecha de vencimiento cuando corresponda y documentar productos descartados.
5. **Cierre diario de caja:** consolidar cobros, pagos y diferencias entre efectivo esperado y efectivo contado cuando esos datos estén disponibles.
6. **Reportes internos:** consultar resúmenes semanales, tablas e historial de reportes dentro de la misma aplicación.

### Exclusiones explícitas

- **No desarrollar costo por receta, rendimiento por elote, gramajes por porción ni cálculo de utilidad por producto.** El propietario no ha proporcionado esos datos.
- No atribuir al negocio ventas diarias, compras, consumos o ganancias que no se conocen.
- No requiere inicio de sesión, autenticación, múltiples usuarios o perfiles.
- No requiere hosting, servidor remoto, servicios en la nube, conexión a internet ni sincronización entre equipos.
- No se necesita versión para celular ni despliegue web.
- **No generar reportes Excel ni CSV como función principal.** Los reportes serán vistas interactivas guardadas en la base de datos.
- No integrar facturación electrónica, pagos con tarjeta, pedidos online o funciones de inteligencia artificial.

## 3. Tecnologías elegidas

| Capa | Tecnología | Propósito |
| --- | --- | --- |
| Interfaz | HTML, CSS y JavaScript | Pantallas y tablas de la aplicación |
| Ventana de escritorio | pywebview | Mostrar la interfaz HTML en una ventana de Windows |
| Lógica local | Python | Validaciones, operaciones y acceso a datos |
| Comunicación | Puente JavaScript–Python de pywebview | Invocar funciones Python desde la interfaz, sin API ni servidor HTTP |
| Persistencia | SQLite mediante `sqlite3` de Python | Guardar datos en un archivo local |
| Distribución | PyInstaller en modo `--onedir` | Empaquetar el ejecutable y sus dependencias en una carpeta |

Los recursos necesarios se incorporarán localmente, sin dependencias de CDN. En Windows se comprobará previamente la disponibilidad del runtime WebView2 que pueda necesitar pywebview.

### ¿El archivo .exe es temporal?

**No.** El archivo `MaizUrbano.exe` permanece en la carpeta de distribución hasta que se elimine. Al hacer doble clic comienza el proceso de la aplicación; al cerrar la ventana ese proceso termina. La base de datos **no se elimina** al cerrar.

Se prioriza la distribución `--onedir`: no requiere instalador propio ni un servidor permanentemente encendido. Las dependencias se mantienen junto al ejecutable. Es posible que Windows necesite el runtime WebView2 instalado previamente.

## 4. Estructura prevista del proyecto

> **Árbol propuesto, no implementado todavía.** Los archivos y directorios siguientes describen la arquitectura deseada; el repositorio no contiene aún el software.

```text
Maiz-Urbano/
├── README.md                   # Contexto, alcance y arquitectura
├── .gitignore                  # Excluye bases de datos, respaldos y builds
├── requirements.txt            # Dependencias Python fijadas al implementar
├── main.py                     # Inicio de la ventana pywebview
│
├── app/                        # Lógica Python
│   ├── __init__.py
│   ├── bridge.py               # Métodos expuestos a JavaScript
│   ├── database.py             # Conexión, esquema e inicialización SQLite
│   └── services/
│       ├── sales.py            # Ventas
│       ├── purchases.py        # Compras y gastos
│       ├── inventory.py        # Inventario, vencimientos y mermas
│       ├── cash.py             # Apertura y cierre de caja
│       └── reports.py          # Generación y consulta de reportes internos
│
├── frontend/                   # Interfaz HTML/CSS/JS local
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   ├── modules/
│   │   ├── sales.js
│   │   ├── purchases.js
│   │   ├── inventory.js
│   │   ├── cash.js
│   │   └── reports.js
│   └── assets/
│       └── brand/              # Recursos visuales autorizados
│
├── data/                       # Creada al ejecutar; NO versionar
│   └── maiz_urbano.db           # Base de datos persistente
│
├── backups/                    # Respaldos locales; NO versionar
│
└── dist/                       # Generada al empaquetar; NO versionar
    └── MaizUrbano/
        ├── MaizUrbano.exe      # Archivo que se abre para la exposición
        ├── _internal/          # Dependencias empaquetadas
        ├── frontend/           # Interfaz incluida en la distribución
        └── data/               # BD creada/utilizada junto al ejecutable
```

En desarrollo, `data/maiz_urbano.db` vivirá junto al código. En la versión empaquetada, se configurará la ruta para que la BD se escriba en `dist/MaizUrbano/data/`, **no** en una carpeta temporal ni dentro de `_internal/`. Esa carpeta debe tener permisos de escritura. Al mover la aplicación, es necesario conservar también `data/` si se desean preservar los registros.

El árbol exacto puede ajustarse durante la implementación sin alterar las decisiones de funcionamiento.

## 5. Modelo de datos inicial (conceptual)

El esquema SQL definitivo se diseñará antes de programar los módulos. Entidades propuestas:

| Entidad | Información principal |
| --- | --- |
| `products` | Catálogo y precios de venta |
| `sales` | Fecha, cobro, total, estado de la operación |
| `sale_items` | Producto, cantidad y precio al momento de la venta |
| `inventory_items` | Insumos, unidades de medida y categorías |
| `stock_entries` | Ingresos individuales, cantidad, fecha y caducidad opcional |
| `stock_movements` | Entradas, consumos, ajustes y mermas, con motivo |
| `purchases` | Abastecimiento registrado y datos conocidos de la compra |
| `expenses` | Gastos generales y forma de pago cuando se conozca |
| `cash_sessions` | Apertura, cierre, cobros, movimientos y diferencias |
| `saved_reports` | Periodo, fecha de generación y contenido del reporte guardado |

**Regla importante:** vender una preparación de elote **no descontará automáticamente** cantidades de crema, queso o elote que no hayan sido verificadas. Para artículos empaquetados podrá descontarse una unidad por venta si esa equivalencia 1:1 se configura explícitamente. Los cambios de existencias se registrarán de forma manual o mediante relaciones comprobadas.

El inventario diferenciará perecederos, no perecederos, productos empaquetados y materiales desechables. Cada ingreso puede tener una fecha de vencimiento independiente; las alertas no sustituyen los criterios de inocuidad alimentaria.

## 6. Interfaz y navegación previstas

Se propone un menú principal sencillo:

- **Inicio:** indicadores del día y accesos rápidos.
- **Ventas:** registro de ventas del menú.
- **Inventario:** entradas, existencias, vencimientos, ajustes y mermas.
- **Compras y gastos:** historial y alta de movimientos.
- **Caja:** jornada actual, cierre y consulta de cierres anteriores.
- **Reportes:** listado histórico, apertura y cierre de tablas de resumen.

La identidad visual partirá de los materiales proporcionados de Maíz Urbano, priorizando legibilidad y una presentación clara para la clase de economía.

### Reportes dentro de la plataforma — decisión aprobada

Los reportes **se visualizan dentro de la aplicación**, no mediante un archivo Excel. Flujo deseado:

1. Abrir el apartado **Reportes**.
2. Ver un historial organizado por semanas, con rango de fechas y fecha de generación.
3. Seleccionar **Ver reporte** para abrir el resumen elegido.
4. Consultar tablas similares a una hoja de cálculo: ventas por día, unidades vendidas, productos más vendidos, compras/gastos registrados, movimientos de inventario y mermas.
5. Pulsar **Cerrar reporte** o **Volver a reportes** para regresar al historial sin cerrar la aplicación.
6. Poder abrir otros reportes guardados y consultarlos aun después de reiniciar el programa.

Para que exista un historial estable, **cada reporte generado se guardará como una fotografía de los datos de ese momento** en SQLite. Si posteriormente se corrigen ventas del periodo, el reporte anterior no cambiará silenciosamente: se podrá generar una nueva versión con su fecha de creación. El periodo semanal predeterminado será **lunes a domingo**, con opción de seleccionar fechas en una iteración posterior.

**No mostrar utilidades netas o costos por receta no sustentados.** Los reportes distinguirán ingresos por ventas, egresos documentados y datos faltantes. No equipararán automáticamente ventas menos compras con ganancia.

## 7. Datos de demostración

Los datos reales de ventas, costos de compra y consumos no se conocen. Si se necesita poblar la aplicación para la exposición:

- Crear un conjunto de operaciones **ficticias y claramente señaladas como datos de demostración**.
- Mantener el menú y los precios compartidos como referencias iniciales, sujetos a confirmación.
- Añadir una opción de **restablecer datos de demostración** con confirmación explícita.
- Evitar que los ejemplos se presenten como resultados económicos reales del negocio.

## 8. Funcionamiento sin conexión, persistencia y respaldos

- Todas las pantallas y librerías necesarias se almacenarán localmente.
- SQLite funciona dentro de la aplicación: no hay que iniciar MySQL, PostgreSQL ni ningún servidor.
- El programa debe crear la carpeta `data/` y el archivo SQLite si aún no existen.
- Toda operación de venta, compra o movimiento debe validarse y guardarse mediante una transacción.
- Al cerrar la ventana, el proceso termina, pero los datos siguen almacenados.
- Se contemplará una función de **crear respaldo local** empleando el mecanismo seguro de backup de SQLite, no la copia indiscriminada de un archivo potencialmente en uso.
- Los datos reales y respaldos no deben subirse accidentalmente a GitHub.

## 9. Orden de implementación sugerido

1. Definir y aprobar pantallas y flujos de interacción.
2. Crear el esqueleto HTML/CSS/JS y la ventana pywebview.
3. Inicializar SQLite y las entidades mínimas.
4. Implementar ventas, compras y gastos.
5. Incorporar inventario, caducidades y mermas sin recetas inventadas.
6. Implementar caja y reportes guardados con tablas internas.
7. Preparar datos ficticios para la demostración y probar cierres/reaperturas.
8. Empaquetar con PyInstaller (`--onedir`) y verificar la ejecución totalmente offline en Windows.

## 10. Estado del repositorio

Este README conserva las decisiones vigentes. **Ya existe la primera implementación de código** en `main.py`, `frontend/`, `tests/` y los archivos de instalación. El árbol de la sección 4 es conceptual y no coincide exactamente con esta primera versión, que centraliza el backend en `main.py`. Se validaron seis pruebas Python/SQLite y la visualización en Chromium; falta la verificación nativa de Windows.

## 11. Referencias técnicas

- [pywebview: uso y comunicación JavaScript–Python](https://pywebview.flowrl.com/guide/usage.html)
- [SQLite en Python: módulo sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [PyInstaller: modos de empaquetado](https://pyinstaller.org/en/stable/operating-mode.html)
- [SQLite: documentación técnica](https://www.sqlite.org/docs.html)


## Ubicaciones correctas y compilación automática

En modo desarrollo, HTML/CSS/JS se encuentran en `frontend/` y SQLite en `data/`. Al empaquetar con PyInstaller `--onedir`, la interfaz reside en `_internal/frontend/` y los datos permanecen en `data/maiz_urbano.db`, al lado de `MaizUrbano.exe`. No copies solo el ejecutable: conserva toda la carpeta.

Para comprobar rutas y almacenamiento sin iniciar la interfaz:

```powershell
py main.py --self-check
py -m unittest discover -s tests -v
```

Para construir la distribución en Windows, ejecuta `powershell -ExecutionPolicy Bypass -File .\build_windows.ps1` en la raíz del proyecto. El script descarga dependencias de desarrollo inicialmente; la app empaquetada no requiere internet.

En GitHub se añadió **Actions → Windows - Compilacion y pruebas**. Cuando se ejecute correctamente podrás descargar el artefacto **MaizUrbano-Windows-portable** y descomprimirlo antes de abrir el `.exe`.

**Estado de validación:** las pruebas de rutas y SQLite se realizaron fuera de Windows. Hasta comprobar una ejecución exitosa en GitHub Actions y abrir la ventana con WebView2, no se considera verificada la aplicación nativa.
