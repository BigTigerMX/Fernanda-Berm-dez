# -*- coding: utf-8 -*-
"""Currículum de Fernanda Ramos en PDF, español e inglés.

Dos lectores a la vez:
 · El filtro automático (ATS): una sola columna, encabezados de siempre, texto real en orden de lectura,
   fechas pegadas a su puesto, nada de tablas. La comprobación del final no es de fe: extrae el texto del
   PDF y revisa cada puesto, el orden de los encabezados, el borde derecho y el tipo de fuente.
 · La persona: la misma marca que el sitio —verde esmeralda, latón, Newsreader e Instrument Sans—, pero
   en blanco para que se imprima bien.

Primero intenta UNA página (lo que prefiere quien recluta); si no cabe a un tamaño legible, va a dos.
Tipografía en instancias ESTÁTICAS (hacer_fuentes.py): con la variable, Chromium incrusta Type 3."""
import html, json, pathlib, re, subprocess, sys
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from contenido import DATOS, ES, EN   # noqa: E402
G = json.loads((AQUI / "glifos.json").read_text())
F = AQUI / "fuentes" / "pdf"
TRAB = AQUI / "cv-trabajo"; TRAB.mkdir(exist_ok=True)
SALE = AQUI / "sitio" / "cv"; SALE.mkdir(parents=True, exist_ok=True)
e = html.escape
MINIMO_UNA = 0.88     # por debajo de esta escala la letra ya es chica: mejor dos páginas

CSS = """
@font-face { font-family: "Newsreader CV"; src: url("file://%(F)s/NewsreaderCV-Medium.ttf"); font-weight: 500; }
@font-face { font-family: "Newsreader CV"; src: url("file://%(F)s/NewsreaderCV-Italic.ttf"); font-weight: 400; font-style: italic; }
@font-face { font-family: "Instrument CV"; src: url("file://%(F)s/InstrumentCV-Regular.ttf"); font-weight: 400; }
@font-face { font-family: "Instrument CV"; src: url("file://%(F)s/InstrumentCV-Medium.ttf"); font-weight: 500; }
@font-face { font-family: "Instrument CV"; src: url("file://%(F)s/InstrumentCV-SemiBold.ttf"); font-weight: 600; }
@page { size: 8.5in 11in; margin: .5in 0 .45in; }
@page :first { margin-top: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { width: 8.5in; font: 400 calc(9.3pt * var(--k)) / 1.36 "Instrument CV", sans-serif; color: #26302B; font-feature-settings: "liga" 0; }
a { color: inherit; text-decoration: none; }
.hoja { width: 8.5in; }
.franja { height: .16in; background: #0B2219; border-bottom: 2pt solid #C9A86A; }
.cab { position: relative; padding: calc(.3in * var(--k)) .6in calc(.16in * var(--k)); }
.mono { position: absolute; right: .55in; top: calc(.22in * var(--k)); width: 1.05in; }
h1 { font: 500 calc(30pt * var(--k)) / 1 "Newsreader CV", serif; letter-spacing: -.015em; color: #0B2219; }
.titulo { margin-top: calc(5pt * var(--k)); font-weight: 600; font-size: calc(9.2pt * var(--k)); letter-spacing: .05em; text-transform: uppercase; color: #145A43; max-width: 6.1in; }
.contacto { margin-top: calc(7pt * var(--k)); font-size: calc(9pt * var(--k)); color: #33403A; }
.contacto i { font-style: normal; color: #B08A48; padding: 0 .5em; }
.cuerpo { padding: 0 .6in; }
h2 { display: flex; align-items: center; gap: 7pt; margin: calc(10pt * var(--k)) 0 calc(4.5pt * var(--k)); font: 600 calc(9.3pt * var(--k)) / 1 "Instrument CV", sans-serif; letter-spacing: .06em; text-transform: uppercase; color: #0F3D2E; }
h2::before { content: ""; width: 5pt; height: 8pt; border-radius: 100%% 0 100%% 0; background: #C9A86A; transform: rotate(12deg); }
h2::after { content: ""; flex: 1; height: .6pt; background: #C6D2CB; }
.perfil { color: #26302B; }
.comp p { margin-bottom: calc(1.4pt * var(--k)); }
.comp b, .idi b { font-weight: 600; color: #0F3D2E; }
.puesto { margin-top: calc(6.5pt * var(--k)); break-inside: avoid; }
.puesto:first-of-type { margin-top: 0; }
.puesto__cab { display: flex; justify-content: space-between; align-items: baseline; gap: 12pt; }
h3 { font: 600 calc(10.2pt * var(--k)) / 1.25 "Instrument CV", sans-serif; color: #0B2219; }
h3 span { font-weight: 500; color: #145A43; }
.fechas { flex: none; font-weight: 500; font-size: calc(8.8pt * var(--k)); color: #4E5C55; white-space: nowrap; }
.area { font: italic 400 calc(9.6pt * var(--k)) / 1.3 "Newsreader CV", serif; color: #3F5A4D; }
ul { list-style: none; margin-top: calc(1.6pt * var(--k)); }
li { position: relative; padding-left: 10pt; margin-top: calc(1pt * var(--k)); }
li::before { content: ""; position: absolute; left: 1.5pt; top: .55em; width: 3.4pt; height: 3.4pt; border-radius: 50%%; background: #B08A48; }
.linea { display: flex; justify-content: space-between; align-items: baseline; gap: 12pt; margin-bottom: calc(1.6pt * var(--k)); }
.linea b { font-weight: 600; color: #0B2219; }
.idi span + span::before { content: "   ·   "; color: #8A978F; white-space: pre; }
"""

def pagina(d, k):
    c = DATOS
    mono = (f'<svg class="mono" viewBox="-140 -1560 2320 1900" aria-hidden="true">'
            f'<path d="{G["F"]["d"]}" transform="scale(1 -1)" fill="#0B2219" fill-opacity=".09"/>'
            f'<path d="{G["R"]["d"]}" transform="translate(860 300) scale(1 -1)" fill="#C9A86A" fill-opacity=".3"/></svg>')
    contacto = " <i>|</i> ".join([f'<a href="{c["tel_href"]}">{e(c["tel"])}</a>', f'<a href="mailto:{c["correo"]}">{e(c["correo"])}</a>'])
    comp = "".join(f"<p><b>{e(r)}:</b> {e(v)}</p>" for r, v in d["comp"])
    exp = ""
    for p in d["exp"]:
        puntos = "".join(f"<li>{e(x)}</li>" for x in p["puntos"])
        exp += (f'<div class="puesto"><div class="puesto__cab"><h3>{e(p["puesto"])} <span>| {e(p["empresa"])}</span></h3>'
                f'<p class="fechas">{e(p["fechas"])}</p></div><p class="area">{e(p["area"])}</p><ul>{puntos}</ul></div>')
    linea = lambda a, b, f: f'<p class="linea"><span><b>{e(a)}</b> | {e(b)}</span><span class="fechas">{e(f)}</span></p>'
    edu = "".join(linea(*x) for x in d["edu"])
    cert = "".join(linea(*x) for x in d["cert"])
    idi = "".join(f"<span><b>{e(a)}:</b> {e(b)}</span>" for a, b in d["idi"])
    return f"""<!doctype html><html lang="{d['lang']}"><head><meta charset="utf-8">
<title>{e(c['nombre'])} — {e(d['titulo'])}</title><meta name="author" content="{e(c['nombre'])}">
<style>:root {{ --k: {k}; }}{CSS % {'F': F}}</style></head><body><div class="hoja">
<div class="franja"></div>
<header class="cab">{mono}<h1>{e(c['nombre'])}</h1><p class="titulo">{e(d['titulo'])} | {e(d['bajada'])}</p><p class="contacto">{contacto}</p></header>
<main class="cuerpo">
<section><h2>{e(d['h_perfil'])}</h2><p class="perfil">{e(d['perfil'])}</p></section>
<section class="comp"><h2>{e(d['h_comp'])}</h2>{comp}</section>
<section><h2>{e(d['h_exp'])}</h2>{exp}</section>
<section><h2>{e(d['h_edu'])}</h2>{edu}</section>
<section><h2>{e(d['h_cert'])}</h2>{cert}</section>
<section class="idi"><h2>{e(d['h_idi'])}</h2><p>{idi}</p></section>
</main></div></body></html>"""

def paginas(pdf):
    return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))

def render(d, k, base):
    h = TRAB / f"{base}.html"; pdf = SALE / f"{base}.pdf"; h.write_text(pagina(d, k))
    alto = int(subprocess.run(["node", str(AQUI / "pdf.cjs"), str(h), str(pdf), str(TRAB / f"{base}.png")], capture_output=True, text=True).stdout.strip() or 0)
    return pdf, alto

def construir(d):
    base = f"cv-fernanda-ramos-{d['lang']}"
    for paso in range(0, 30):            # una página: el mayor tamaño que quepa con margen inferior digno
        k = round(1.06 - paso * 0.01, 2)
        if k < MINIMO_UNA: break
        pdf, alto = render(d, k, base)
        if alto <= 1056 - 30 and paginas(pdf) == 1: return pdf, k, alto
    for k in (1.1, 1.08, 1.06, 1.04, 1.02, 1.0):   # no cupo legible: dos páginas, al mayor tamaño que siga en dos
        pdf, alto = render(d, k, base)
        if paginas(pdf) == 2: return pdf, k, alto
    return pdf, k, alto

def comprobar(pdf, d):
    txt = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"], capture_output=True, text=True).stdout
    lineas = [l.strip() for l in txt.splitlines() if l.strip()]
    fallas = []
    if any(0xE000 <= ord(ch) <= 0xF8FF for ch in txt): fallas.append("caracteres de uso privado")
    for dato in (DATOS["tel"], DATOS["correo"], DATOS["nombre"], d["titulo"].upper()):
        if dato not in txt: fallas.append(f"no se extrae: {dato}")
    cajas = subprocess.run(["pdftotext", "-bbox", str(pdf), "-"], capture_output=True, text=True).stdout
    fuera = [m for m in re.findall(r'xMax="([\d.]+)"', cajas) if float(m) > 612 - 20]
    if fuera: fallas.append(f"{len(fuera)} palabras tocan o pasan el borde derecho")
    for p in d["exp"]:
        try:
            i = next(n for n, l in enumerate(lineas) if p["puesto"][:30] in l)
            j = next(n for n, l in enumerate(lineas) if p["fechas"] in l and n >= i - 1)
            b = next(n for n, l in enumerate(lineas) if p["puntos"][0][:30] in l and n >= i)
            if not (abs(j - i) <= 3 and j < b + 1): fallas.append(f"fechas lejos de «{p['puesto']}» ({i},{j},{b})")
        except StopIteration: fallas.append(f"no se encontró «{p['puesto']}» o sus fechas")
    orden = [next((n for n, l in enumerate(lineas) if t.upper() in l.upper()), -1) for t in (d["h_perfil"], d["h_comp"], d["h_exp"], d["h_edu"], d["h_cert"], d["h_idi"])]
    if orden != sorted(orden) or -1 in orden: fallas.append(f"encabezados fuera de orden {orden}")
    tipos = sorted(set(re.findall(r"(Type 3|CID TrueType|TrueType|CID Type 0C|Type 1C?)", subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout)))
    if "Type 3" in tipos: fallas.append("hay fuentes Type 3")
    return fallas, tipos, len(txt.split())

if __name__ == "__main__":
    for d in (ES, EN):
        pdf, k, alto = construir(d)
        fallas, tipos, palabras = comprobar(pdf, d)
        print(f"{pdf.name}  {pdf.stat().st_size:,} bytes · {paginas(pdf)} pág · escala {k} · alto {alto} px · {palabras} palabras · fuentes {tipos} · ATS: {'OK' if not fallas else fallas}")
