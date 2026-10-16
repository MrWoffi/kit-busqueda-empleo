"""Muestra la descripción completa de uno o varios avisos (Computrabajo, LinkedIn o Get on Board).
    python herramientas/detalle.py <url o id> [<url o id> ...]
Acepta la URL del aviso o el id que aparece en la búsqueda (ct-..., li-..., gob-...).
"""
import html, re, sys, time
from comun import descargar


def limpio(t):
    t = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", "", t or "")
    t = re.sub(r"<br\s*/?>|</p>|</li>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", html.unescape(t))).strip()


def computrabajo(url):
    s = descargar(url)
    if not s:
        return ""
    t = limpio(s)
    i, j = t.find("Descripción de la oferta"), t.find("Palabras clave")
    return t[i:j] if i >= 0 and j > i else t[i:i + 4000] if i >= 0 else "No se encontró la descripción (el aviso puede estar cerrado)."


def linkedin(numero):
    s = descargar("https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/" + numero)
    if not s:
        return ("LinkedIn no entregó el aviso (suele pasar justo después de una búsqueda). Leerlo con el navegador "
                f"conectado: linkedin.com/jobs/view/{numero}, botón 'más' y bloque 'Acerca del empleo'. O reintentar en una hora.")
    d = re.search(r"show-more-less-html__markup[^>]*>([\s\S]*?)</div>", s)
    criterios = re.findall(r'description__job-criteria-subheader">([\s\S]*?)</h3>[\s\S]*?criteria-text[^>]*>([\s\S]*?)</span>', s)
    extra = "\n".join(f"{limpio(a)}: {limpio(b)}" for a, b in criterios)
    return (limpio(d.group(1)) if d else "No se encontró la descripción.") + ("\n\n" + extra if extra else "")


def getonboard(slug):
    s = descargar("https://www.getonbrd.com/jobs/" + slug)
    if not s:
        return ""
    partes = []
    for m in re.finditer(r'<div[^>]*itemprop="(?:description|responsibilities|qualifications|jobBenefits)"[^>]*>', s):
        nivel, pos = 1, m.end()
        for etiqueta in re.finditer(r"<(/?)div\b", s[pos:]):
            nivel += -1 if etiqueta.group(1) else 1
            if nivel == 0:
                partes.append(s[pos:pos + etiqueta.start()])
                break
    return "\n\n".join(limpio(x) for x in partes) or "No se encontró la descripción."


def main():
    linkedin_previos = 0
    for x in sys.argv[1:]:
        if x.startswith("li-") or "linkedin.com" in x:
            if linkedin_previos:
                time.sleep(2.5)
            linkedin_previos += 1
            numero = re.search(r"(\d{6,})", x)
            texto = linkedin(numero.group(1)) if numero else "No reconozco ese id de LinkedIn. Usa el de la búsqueda (li-123...) o la URL del aviso."
        elif x.startswith("gob-") or "getonbrd.com" in x:
            texto = getonboard(x[4:] if x.startswith("gob-") else x.rstrip("/").split("/")[-1])
        elif x.startswith("ct-"):
            print(f"===== {x}\nPara Computrabajo pasa la URL completa (columna url de la búsqueda).\n")
            continue
        else:
            texto = computrabajo(x)
        print(f"===== {x}\n{texto[:6000]}\n")


if __name__ == "__main__":
    main()
