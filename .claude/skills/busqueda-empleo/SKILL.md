---
name: busqueda-empleo
description: "Busca, evalúa y ayuda a postular a empleos (Computrabajo, LinkedIn, Get on Board) con un perfil verificado que impide inventar experiencia, una rúbrica para decidir, un tracker de postulaciones, CV en PDF, preparación de entrevistas y seguimiento. Usar cuando la persona salude por primera vez, diga 'busca ofertas', 'postula a este aviso', 'arma mi CV', 'me llamaron de X', 'prepárame la entrevista', 'cómo van mis postulaciones', o pegue el enlace de un aviso."
---

# Búsqueda de empleo

Kit de Altrion Partners (altrionpartners.com), licencia MIT. El método de perfil verificado, rúbrica y tracker está adaptado de [ai-job-search](https://github.com/MadsLorentzen/ai-job-search) (MIT).

## Piezas

| Archivo | Para qué | Cuándo se lee |
|---|---|---|
| `mis-datos/perfil.md` | Hechos verificados de la persona, herramientas con nivel, lo que NO tiene, qué busca | Antes de cualquier CV, respuesta o mensaje |
| `mis-datos/config.json` | Palabras clave, ciudades, sueldo mínimo, zonas excluidas | Lo usan los scripts de búsqueda |
| `perfil-plantilla.md` | Estructura del perfil | Solo en la configuración inicial |
| `reglas-formularios.md` | Cómo responder lo que falta, grado, sueldo, ubicación, datos personales, estilo | Antes de cada postulación |
| `rubrica.md` | Filtros duros y puntaje 0-100 | Al evaluar cada aviso |
| `entrevista.md` | Guía de entrevista y simulacro | Cuando una empresa llama o agenda |
| `seguimiento.md` | Estados del tracker, seguimiento y limpieza | En cada revisión |

## Configuración inicial (primera vez)

1. Si la persona dejó su CV en `mis-datos/`, léelo primero (PDF) y saca de ahí lo que puedas.
2. Entrevista corta, **una pregunta a la vez**, para completar `perfil-plantilla.md`:
   - Nombre, ciudad, celular, correo, LinkedIn. Nunca el documento de identidad.
   - Estudios: carrera, institución, estado exacto (estudiante, egresado, bachiller, titulado) y fecha.
   - Cada trabajo: empresa, cargo, fechas, qué hacía y **un resultado con número si existe** (cuánto, cuántos, en cuánto tiempo). Si no hay número, no se inventa.
   - Cursos y certificados (con institución y año), idiomas con nivel real.
   - Herramientas con nivel honesto. Pregunta también **qué NO maneja** de lo que suelen pedir en su rubro.
   - Qué busca: puestos, ciudades, remoto o presencial, sueldo mínimo, zonas donde no trabajaría, edad si los avisos de su país la piden.
3. Escribe `mis-datos/perfil.md` y muéstraselo para que lo confirme.
4. Escribe `mis-datos/config.json` a partir de `config.ejemplo.json`:
   - `pais`: el subdominio de Computrabajo (pe, mx, co, cl, ar, ec...).
   - `ciudades[].computrabajo`: la **región o departamento** como aparece en la URL del portal (lima, la-libertad, arequipa, jalisco, bogota-dc). Comprobar con una búsqueda que el título de la página diga esa región.
   - `ciudades[].linkedin`: como lo escribe LinkedIn ("Lima, Peru").
   - `palabras_clave`: 5 a 12 nombres de puesto reales del rubro.
5. CV general: copia `plantillas/cv.html` a `mis-datos/cvs/cv-general.html`, llénalo solo con datos del perfil, genera el PDF (`python herramientas/generar_pdf.py mis-datos/cvs/cv-general.html`), **ábrelo y míralo**: una página, nada cortado. Muéstraselo.

## Revisión diaria

1. `python herramientas/buscar.py` (los tres portales; quita los ya registrados y las palabras excluidas). Guarda la lista en `mis-datos/busquedas/`.
2. Lee el título, empresa, ubicación y sueldo de cada aviso. Para los que pasan a primera vista, `python herramientas/detalle.py <url o id>`.
3. Aplica `rubrica.md`: filtros duros primero, después puntaje. Registra también los descartados con su razón: `python herramientas/tracker.py agregar <id> --estado descartado --notas "razón"`.
4. Muestra a la persona una tabla corta: puesto, empresa, puntaje, por qué. Ella elige.
5. Por cada aviso elegido, postula según la sección siguiente y registra: `python herramientas/tracker.py agregar <id> --puntaje N --sueldo X --cv cvs/archivo.pdf`.
6. Cierra con el resumen: enviadas hoy, procesos vivos y lo que necesita de ella.

## Postular

Dos formas. Pregunta cuál prefiere la primera vez y respeta esa elección.

- **A. La persona postula y tú preparas.** Le das cada respuesta del formulario lista para copiar, el CV indicado y, si piden carta, una de 4 a 6 líneas. Ella pega y envía.
- **B. Con el navegador conectado** (en VS Code escribe `@browser`; requiere la extensión Claude in Chrome). La persona inicia sesión en el portal ella misma. Tú abres el aviso, llenas el formulario y **te detienes antes de Enviar**: muestras las respuestas, ella revisa y aprieta el botón, o te autoriza a hacerlo para ese aviso.
  - En LinkedIn, un aviso a la vez y con la persona presente. Sin ráfagas ni envíos masivos: va contra sus condiciones de uso y puede restringir la cuenta.
  - Si aparece un captcha o un inicio de sesión, lo resuelve la persona.

En ambas formas, antes de enviar, revisa cada respuesta contra `perfil.md` y `reglas-formularios.md`.

**CV por aviso:** si el puntaje es 75 o más, conviene una versión ajustada (mismo contenido verdadero, otro orden y énfasis, palabras del aviso solo donde describen algo que la persona sí hizo). Guárdala en `mis-datos/cvs/<empresa>-<puesto>.html` y su PDF.

## Qué lee y qué escribe

| Cuándo | Lee | Escribe |
|---|---|---|
| Cada revisión | `mis-datos/config.json`, `mis-datos/tracker.csv` | `mis-datos/busquedas/AAAA-MM-DD.csv`, filas del tracker |
| La persona confirma un dato nuevo | — | `mis-datos/perfil.md` en el mismo momento, con fecha |
| Se descubre una respuesta mal dada | — | La regla en `reglas-formularios.md` para que no se repita |
| Llaman de una empresa | Aviso, CV enviado, perfil | `mis-datos/entrevistas/<empresa>-<puesto>.md` |

## Herramientas (`herramientas/`)

- `buscar.py [portal]`: avisos nuevos de Computrabajo, LinkedIn y Get on Board. Pausas entre consultas. Si un portal responde 429 (demasiadas consultas), esa búsqueda se detiene: no reintentar el mismo día.
- `detalle.py <url o id>`: descripción completa del aviso.
- `tracker.py agregar | estado | resumen | limpieza`: registro de postulaciones.
- `generar_pdf.py <html> [pdf]`: CV a PDF con Chrome o Edge.

## Reglas que no se negocian

- Nada se afirma si no está en `perfil.md`.
- Ninguna postulación ni mensaje sale sin aprobación de la persona.
- Nunca el documento de identidad, nunca cuentas nuevas, nunca un grado que no tiene.
- Una respuesta equivocada se corrige en la regla que la produjo, no solo en ese aviso.
