# Rúbrica para decidir si se postula

Adaptada de ai-job-search (MIT, Mads Lorentzen). Primero los filtros duros, después el puntaje. Los valores (sueldo mínimo, ciudades, zonas) salen de `mis-datos/perfil.md` y `mis-datos/config.json`.

## 1. Filtros duros (si uno falla, no se postula)

| Filtro | Falla cuando |
|---|---|
| Sueldo | El aviso fija un monto bajo el mínimo de esa ciudad (contar el total fijo: básico más bonos fijos) |
| Ubicación | Fuera de las ciudades del perfil, o en una zona excluida |
| Idioma | Pide un nivel mayor al que la persona tiene, o entrevistas en ese idioma si no puede sostenerlas |
| Edad | El aviso marca un rango que no incluye la edad de la persona |
| Requisito indispensable | Pide como obligatorio algo que está en "Lo que NO tiene" (una herramienta, un título, una colegiatura) |
| Experiencia | Pide bastante más de lo que tiene, o el cargo es de jefatura cuando la persona no la ha tenido |
| Ya postulado | El id ya está en el tracker |
| Forma de postular | Exige crear cuenta en otro sitio: no se descarta, pasa a la lista de pendientes de la persona |

Marca de alerta (se postula, pero se avisa): pide uno o dos años más de los que tiene, un grado como deseable, una herramienta deseable que no tiene, turnos de fin de semana, viajes.

## 2. Puntaje (0 a 100)

| Dimensión | Peso | Qué mide |
|---|---|---|
| Técnica | 30 % | Cuántas de las herramientas pedidas tiene al nivel suficiente según el perfil |
| Experiencia | 25 % | Si hizo la función (no importa el nombre del cargo) |
| Encaje | 15 % | Modalidad, horario, tamaño y tipo de empresa compatibles con lo que busca |
| Dirección | 30 % | Cuánto acerca a su objetivo de carrera |

Bandas por dimensión: 80 o más fuerte, 60 a 79 bueno, 40 a 59 parcial, menos de 40 débil.

## 3. Decisión

| Puntaje | Qué se hace |
|---|---|
| 75 o más | Postular hoy, con CV ajustado y respuestas escritas para ese aviso |
| 60 a 74 | Postular con el CV general, revisando cada respuesta |
| 45 a 59 | Postular solo si ese día no hay mejores |
| Menos de 45 | No postular |

El puntaje va en la columna `puntaje` del tracker y la razón principal en `notas`.
