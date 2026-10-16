# Seguimiento de postulaciones

## Estados del tracker

| Estado | Cuándo |
|---|---|
| `postulado` | Enviado, sin señal |
| `cv_visto` | El portal marca el CV como visto |
| `en_proceso` | Llamada, mensaje, entrevista agendada o pedido de documentos |
| `entrevista` | Entrevista hecha |
| `oferta` | Propuesta de sueldo o preoferta |
| `contratado` | Final |
| `finalizado` | El portal cerró el proceso sin elegirla. Final |
| `sin_respuesta` | 60 días sin señal. Final |
| `retirado` | La persona retiró la postulación. Final |
| `descartado` | Evaluado y no postulado (se guarda para no volver a revisarlo) |

Cambiar estado: `python herramientas/tracker.py estado <id> <estado> --notas "qué pasó"`.

## Actualizar estados

- Computrabajo muestra el estado en "Mis postulaciones". Con el navegador conectado se puede leer esa página y actualizar el tracker. Si no, la persona cuenta qué ve.
- LinkedIn no muestra estados confiables: se actualiza cuando llega un mensaje o correo.
- Cada vez que la persona diga "me llamaron de X", "me escribieron", "me rechazaron": actualizar el tracker en ese momento.

## Mensajes de seguimiento

- Si un proceso está en `en_proceso` o `entrevista` y pasan 10 días sin noticias, se redacta un mensaje corto (nombre de pila, dos frases, despedida) y se le muestra a la persona. Nunca se envía solo.
- Máximo dos seguimientos por proceso.

## Limpieza semanal

`python herramientas/tracker.py limpieza` lista lo que lleva más de 60 días en `postulado` o `cv_visto`. Se pasa a `sin_respuesta` solo si la persona lo aprueba.
