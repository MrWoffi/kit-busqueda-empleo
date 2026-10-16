"""Busca avisos nuevos en Computrabajo, LinkedIn y Get on Board según mis-datos/config.json.

Quita los que ya están en el tracker y los que tienen en el título una palabra excluida.
Guarda la lista en mis-datos/busquedas/AAAA-MM-DD.csv y la muestra en pantalla.
    python herramientas/buscar.py                    # los tres portales
    python herramientas/buscar.py computrabajo       # solo uno
"""
import csv, html, re, sys, time, unicodedata, urllib.parse
from comun import DATOS, config, descargar, hoy, leer_tracker


def sin_tildes(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def limpio(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t or ""))).strip()


def ruta(href):
    """El portal escribe algunos enlaces con entidades HTML (&#xA0;) y un ancla de seguimiento (#lc=...)."""
    return urllib.parse.quote(html.unescape(href).split("#")[0], safe="/-_.")


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", sin_tildes(t)).strip("-")


def computrabajo(cfg):
    """Computrabajo busca por departamento o región (lima, la-libertad, arequipa). Remoto no se filtra aquí:
    lo cubren LinkedIn y Get on Board. Se descartan los avisos cuya ubicación no es la región pedida,
    porque el portal también devuelve avisos de otras ciudades cuando la palabra aparece en el texto."""
    pais, dias = cfg["pais"], cfg.get("dias_hacia_atras", 1)
    pubdate = 1 if dias <= 1 else 3 if dias <= 3 else 7
    for kw in cfg["palabras_clave"]:
        for c in cfg["ciudades"]:
            region = c.get("computrabajo")
            if not region:
                continue
            for pagina in (1, 2):
                url = f"https://{pais}.computrabajo.com/trabajo-de-{slug(kw)}-en-{region}?pubdate={pubdate}&p={pagina}"
                s = descargar(url)
                if not s:
                    break
                articulos = re.findall(r"<article[\s\S]*?</article>", s)
                for a in articulos:
                    i = re.search(r"data-id='([0-9A-F]{32})'", a)
                    t = re.search(r'<a class="js-o-link[^"]*" href="([^"]+)">([\s\S]*?)</a>', a)
                    if not i or not t:
                        continue
                    ps = [limpio(p) for p in re.findall(r"<p[^>]*>([\s\S]*?)</p>", a)]
                    ubicacion = ps[1] if len(ps) > 1 else ""
                    if region not in slug(ubicacion):
                        continue
                    sueldo = re.search(r'i_salary"></span>([\s\S]*?)</span>', a)
                    yield {"id": "ct-" + i.group(1), "portal": "computrabajo", "puesto": limpio(t.group(2)),
                           "empresa": re.sub(r"^\d+[.,]\d\s*", "", ps[0]) if ps else "", "ubicacion": ubicacion,
                           "sueldo": limpio(sueldo.group(1)) if sueldo else "", "publicado": ps[-1] if ps else "",
                           "busqueda": kw, "url": f"https://{pais}.computrabajo.com{ruta(t.group(1))}"}
                time.sleep(1.5)
                if len(articulos) < 20:
                    break


def linkedin(cfg):
    segundos = 86400 * max(1, cfg.get("dias_hacia_atras", 1))
    lugares = [(c["linkedin"], None) for c in cfg["ciudades"] if c.get("linkedin")]
    if cfg.get("buscar_remoto") and cfg.get("linkedin_pais"):
        lugares.append((cfg["linkedin_pais"], "2"))
    for kw in cfg["palabras_clave"]:
        for lugar, modalidad in lugares:
            q = {"keywords": kw, "location": lugar, "f_TPR": f"r{segundos}", "start": "0"}
            if modalidad:
                q["f_WT"] = modalidad
            s = descargar("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?" + urllib.parse.urlencode(q))
            if s is None:
                return
            for li in re.findall(r"<li>([\s\S]*?)</li>", s):
                i = re.search(r"jobPosting:(\d+)", li)
                if not i:
                    continue
                g = lambda patron: limpio((re.search(patron, li) or [None, ""])[1])
                yield {"id": "li-" + i.group(1), "portal": "linkedin",
                       "puesto": g(r'base-search-card__title">([\s\S]*?)</h3>'),
                       "empresa": g(r'base-search-card__subtitle">([\s\S]*?)</h4>'),
                       "ubicacion": g(r'job-search-card__location">([\s\S]*?)</span>') + (" (remoto)" if modalidad else ""),
                       "sueldo": g(r'job-search-card__salary-info">([\s\S]*?)</span>'),
                       "publicado": g(r"<time[^>]*>([\s\S]*?)</time>"), "busqueda": kw,
                       "url": "https://www.linkedin.com/jobs/view/" + i.group(1)}
            time.sleep(2.5)


def getonboard(cfg):
    limite = time.time() - 86400 * max(1, cfg.get("dias_hacia_atras", 1))
    for kw in cfg["palabras_clave"]:
        q = {"query": kw, "per_page": 50, "page": 1, "expand": '["company"]'}
        d = descargar("https://www.getonbrd.com/api/v0/search/jobs?" + urllib.parse.urlencode(q), json_=True)
        for j in (d or {}).get("data", []):
            a = j["attributes"]
            if not a.get("published_at") or a["published_at"] < limite:
                continue
            remoto = a.get("remote_modality") == "fully_remote" or a.get("remote") is True
            if not remoto:
                continue
            sueldo = f"USD {a['min_salary']}-{a['max_salary']}" if a.get("min_salary") else ""
            empresa = (((a.get("company") or {}).get("data") or {}).get("attributes") or {}).get("name", "")
            yield {"id": "gob-" + j["id"], "portal": "getonboard", "puesto": a.get("title", ""), "empresa": empresa,
                   "ubicacion": ("Remoto " + "/".join(c for c in (a.get("countries") or []) if c != "Remote")).strip(), "sueldo": sueldo, "publicado": time.strftime("%Y-%m-%d", time.localtime(a["published_at"])),
                   "busqueda": kw, "url": "https://www.getonbrd.com/jobs/" + j["id"]}
        time.sleep(1)


PORTALES = {"computrabajo": computrabajo, "linkedin": linkedin, "getonboard": getonboard}


def main():
    cfg = config()
    elegidos = sys.argv[1:] or list(PORTALES)
    vistos = leer_tracker()
    excluir = [sin_tildes(p) for p in cfg.get("excluir_si_el_titulo_dice", [])]
    zonas = [sin_tildes(z) for z in cfg.get("zonas_excluidas", [])]
    avisos, quitados = {}, {"ya en el tracker": 0, "palabra excluida": 0, "zona excluida": 0}
    for nombre in elegidos:
        print(f"Buscando en {nombre}...")
        for a in PORTALES[nombre](cfg):
            if a["id"] in avisos:
                continue
            titulo = sin_tildes(a["puesto"])
            if a["id"] in vistos:
                quitados["ya en el tracker"] += 1
            elif any(re.search(r"\b" + re.escape(p) + r"\b", titulo) for p in excluir):
                quitados["palabra excluida"] += 1
            elif any(z in sin_tildes(a["ubicacion"]) for z in zonas):
                quitados["zona excluida"] += 1
            else:
                avisos[a["id"]] = a
    carpeta = DATOS / "busquedas"
    carpeta.mkdir(parents=True, exist_ok=True)
    salida = carpeta / f"{hoy()}.csv"
    campos = ["id", "portal", "puesto", "empresa", "ubicacion", "sueldo", "publicado", "busqueda", "url"]
    with salida.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(avisos.values())
    print(f"\n{len(avisos)} avisos nuevos. Quitados: " + ", ".join(f"{v} {k}" for k, v in quitados.items()))
    for a in avisos.values():
        print(f"{a['id'][:14]:14} | {a['puesto'][:55]:55} | {a['empresa'][:28]:28} | {a['ubicacion'][:28]:28} | {a['sueldo'][:22]}")
    print(f"\nGuardado en {salida.relative_to(DATOS.parent)}")


if __name__ == "__main__":
    main()
