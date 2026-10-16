"""Registro de postulaciones en mis-datos/tracker.csv.

    python herramientas/tracker.py agregar <id> --estado postulado --puntaje 72 --sueldo 2500 --cv cvs/general.pdf --notas "..."
        Toma empresa, puesto, ubicación y URL de la última búsqueda guardada (mis-datos/busquedas/).
    python herramientas/tracker.py estado <id> <nuevo_estado> [--notas "..."]
    python herramientas/tracker.py resumen
    python herramientas/tracker.py limpieza          # lista lo que lleva más de 60 días sin señal
"""
import argparse, csv, datetime, sys
from comun import COLUMNAS, DATOS, ESTADOS, hoy, leer_tracker, guardar_tracker

FINALES = {"contratado", "finalizado", "sin_respuesta", "retirado", "descartado"}


def de_busquedas(id_):
    for archivo in sorted((DATOS / "busquedas").glob("*.csv"), reverse=True):
        with archivo.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                if r["id"] == id_:
                    return r
    return {}


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="accion", required=True)
    a = sub.add_parser("agregar")
    a.add_argument("id")
    for campo in ("estado", "puntaje", "sueldo", "cv", "notas", "empresa", "puesto", "ubicacion", "url", "portal"):
        a.add_argument("--" + campo, default="")
    e = sub.add_parser("estado")
    e.add_argument("id")
    e.add_argument("nuevo", choices=ESTADOS)
    e.add_argument("--notas", default="")
    sub.add_parser("resumen")
    sub.add_parser("limpieza")
    args = p.parse_args()
    filas = leer_tracker()

    if args.accion == "agregar":
        estado = args.estado or "postulado"
        if estado not in ESTADOS:
            sys.exit(f"Estado no válido. Usa uno de: {', '.join(ESTADOS)}")
        b = de_busquedas(args.id)
        previa = filas.get(args.id, {})
        if not b and not previa and not args.puesto:
            sys.exit(f"No encontré {args.id} en las búsquedas guardadas. Revisa el id o agrégalo a mano con --puesto, --empresa y --url.")
        fila = {c: previa.get(c, "") for c in COLUMNAS}
        fila.update(id=args.id, fecha=previa.get("fecha") or hoy(), estado=estado, actualizado=hoy(),
                    portal=args.portal or b.get("portal", "") or fila["portal"],
                    empresa=args.empresa or b.get("empresa", "") or fila["empresa"],
                    puesto=args.puesto or b.get("puesto", "") or fila["puesto"],
                    ubicacion=args.ubicacion or b.get("ubicacion", "") or fila["ubicacion"],
                    url=args.url or b.get("url", "") or fila["url"],
                    puntaje=args.puntaje or fila["puntaje"], sueldo_pedido=args.sueldo or fila["sueldo_pedido"],
                    cv=args.cv or fila["cv"], notas=args.notas or fila["notas"])
        filas[args.id] = fila
        guardar_tracker(filas)
        print(f"{'Actualizado' if previa else 'Agregado'}: {fila['puesto']} | {fila['empresa']} | {estado}")

    elif args.accion == "estado":
        if args.id not in filas:
            sys.exit(f"No está en el tracker: {args.id}")
        filas[args.id]["estado"] = args.nuevo
        filas[args.id]["actualizado"] = hoy()
        if args.notas:
            filas[args.id]["notas"] = (filas[args.id]["notas"] + " | " if filas[args.id]["notas"] else "") + f"{hoy()}: {args.notas}"
        guardar_tracker(filas)
        print(f"{filas[args.id]['puesto']} | {filas[args.id]['empresa']} -> {args.nuevo}")

    elif args.accion == "resumen":
        conteo = {}
        for r in filas.values():
            conteo[r["estado"]] = conteo.get(r["estado"], 0) + 1
        enviadas = sum(v for k, v in conteo.items() if k != "descartado")
        print(f"{len(filas)} filas, {enviadas} postulaciones enviadas")
        for estado in ESTADOS:
            if conteo.get(estado):
                print(f"  {estado:14} {conteo[estado]}")
        vivos = [r for r in filas.values() if r["estado"] in ("en_proceso", "entrevista", "oferta")]
        if vivos:
            print("\nProcesos vivos:")
            for r in vivos:
                print(f"  {r['estado']:11} | {r['empresa'][:30]:30} | {r['puesto'][:45]:45} | desde {r['actualizado']}")

    elif args.accion == "limpieza":
        limite = (datetime.date.today() - datetime.timedelta(days=60)).isoformat()
        viejos = [r for r in filas.values() if r["estado"] in ("postulado", "cv_visto") and (r["actualizado"] or r["fecha"]) < limite]
        print(f"{len(viejos)} postulaciones con más de 60 días sin señal (pasarlas a sin_respuesta si la persona lo aprueba):")
        for r in viejos:
            print(f"  {r['id']} | {r['empresa'][:30]} | {r['puesto'][:45]} | {r['fecha']}")


if __name__ == "__main__":
    main()
