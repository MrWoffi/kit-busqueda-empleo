"""Convierte un CV en HTML a PDF con Chrome o Edge (sin instalar nada más).
    python herramientas/generar_pdf.py mis-datos/cvs/cv-general.html            # deja cv-general.pdf al lado
    python herramientas/generar_pdf.py mis-datos/cvs/cv-general.html salida.pdf
"""
import os, pathlib, shutil, subprocess, sys

CANDIDATOS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def navegador():
    for c in CANDIDATOS:
        if os.path.exists(c):
            return c
    for nombre in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge", "chrome"):
        if shutil.which(nombre):
            return shutil.which(nombre)
    sys.exit("No encontré Chrome ni Edge. Instala Google Chrome y vuelve a intentar.")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    origen = pathlib.Path(sys.argv[1]).resolve()
    destino = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else origen.with_suffix(".pdf")
    subprocess.run([navegador(), "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={destino}", origen.as_uri()], check=True, capture_output=True, timeout=90)
    print(f"PDF listo: {destino}")


if __name__ == "__main__":
    main()
