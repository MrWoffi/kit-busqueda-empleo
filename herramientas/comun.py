"""Piezas compartidas: rutas, configuración, descarga de páginas y el tracker."""
import csv, datetime, json, pathlib, sys, time, urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATOS = RAIZ / "mis-datos"
TRACKER = DATOS / "tracker.csv"
COLUMNAS = ["id", "fecha", "portal", "empresa", "puesto", "ubicacion", "estado", "puntaje",
            "sueldo_pedido", "cv", "notas", "url", "actualizado"]
ESTADOS = ["postulado", "cv_visto", "en_proceso", "entrevista", "oferta", "contratado",
           "finalizado", "sin_respuesta", "retirado", "descartado"]
AGENTE = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def config():
    propio = DATOS / "config.json"
    archivo = propio if propio.exists() else RAIZ / "config.ejemplo.json"
    if archivo != propio:
        print("Aviso: no existe mis-datos/config.json, se usa config.ejemplo.json\n")
    return json.loads(archivo.read_text(encoding="utf-8"))


def descargar(url, json_=False, intentos=2):
    for i in range(intentos):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": AGENTE}), timeout=25)
            cuerpo = r.read().decode("utf-8", "ignore")
            return json.loads(cuerpo) if json_ else cuerpo
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"  El portal pidió bajar el ritmo (429). Se detiene esta búsqueda: {url[:80]}")
                return None
            if i == intentos - 1:
                print(f"  Error {e.code}: {url[:80]}")
        except Exception as e:
            if i == intentos - 1:
                print(f"  No se pudo abrir {url[:80]}: {e}")
        time.sleep(2)
    return None


def leer_tracker():
    if not TRACKER.exists():
        return {}
    with TRACKER.open(encoding="utf-8", newline="") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def guardar_tracker(filas):
    DATOS.mkdir(exist_ok=True)
    orden = sorted(filas.values(), key=lambda r: r.get("fecha") or "0000", reverse=True)
    with TRACKER.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS, extrasaction="ignore")
        w.writeheader()
        w.writerows(orden)


def hoy():
    return datetime.date.today().isoformat()
