# Kit de búsqueda de empleo con IA

Un asistente que trabaja contigo en tu búsqueda de empleo, dentro de Claude Code:

- **Arma tu CV** con tus datos reales, en PDF de una página, y lo ajusta para cada puesto sin inventar nada.
- **Busca avisos nuevos cada día** en Computrabajo, LinkedIn y Get on Board, según tus puestos, ciudades y sueldo mínimo.
- **Decide contigo a cuáles postular** con una rúbrica de 0 a 100 y filtros duros (sueldo, zona, idioma, requisitos que no tienes).
- **Prepara las respuestas de cada formulario** y, si conectas el navegador, las llena por ti. Tú revisas y envías.
- **Lleva el registro** de cada postulación y su estado.
- **Prepara tus entrevistas** con preguntas probables y respuestas basadas en tu experiencia real, y hace simulacros.

Creado por **[Altrion Partners](https://altrionpartners.com)**.

## Cómo empezar

1. Necesitas una cuenta de Claude de pago (Pro o superior), Visual Studio Code con la extensión **Claude Code**, Python 3.10 o más y Google Chrome.
2. Descarga este repositorio (botón **Code → Download ZIP**) y descomprímelo en tus Documentos.
3. Abre la carpeta en VS Code, abre Claude Code (ícono de chispa en la barra izquierda) y escribe **hola**.

La guía paso a paso completa, para quien nunca ha usado estas herramientas, está en [`guia/guia-paso-a-paso.pdf`](guia/guia-paso-a-paso.pdf).

## Qué hay dentro

```
CLAUDE.md                         Lo que hace el asistente al decirle "hola"
config.ejemplo.json               Ejemplo de configuración de búsqueda
.claude/skills/busqueda-empleo/   El método: reglas, rúbrica, entrevistas, seguimiento
herramientas/                     Scripts de búsqueda, detalle, tracker y PDF (solo Python estándar)
plantillas/cv.html                Plantilla de CV de una página
guia/                             Guía paso a paso en PDF
mis-datos/                        Tu perfil, tu CV y tu registro. Nunca se sube a GitHub
```

## Privacidad

Todo lo tuyo queda en `mis-datos/`, en tu computadora. Esa carpeta está excluida en `.gitignore`. El asistente nunca escribe tu documento de identidad, no crea cuentas a tu nombre y no envía nada sin tu aprobación.

Si haces una copia de este repositorio en tu GitHub, déjala **privada** si piensas guardar ahí tus datos.

## Límites honestos

- Los portales cambian su diseño sin avisar. Si una búsqueda deja de traer resultados, pídele a Claude que revise el script.
- LinkedIn limita las consultas seguidas. Si responde 429, la búsqueda se detiene y se vuelve a intentar al día siguiente.
- El kit no postula en masa ni de forma automática: cada postulación pasa por ti.

## Créditos y licencia

Licencia MIT. © 2026 Altrion Partners. Cualquier copia o versión modificada debe conservar el aviso de copyright y la licencia (archivo `LICENSE`).

El método de perfil verificado, rúbrica y tracker está adaptado de [ai-job-search](https://github.com/MadsLorentzen/ai-job-search) de Mads Lorentzen (MIT).
