# -*- coding: utf-8 -*-
"""Arma el sitio de Fernanda Ramos desde contenido.py (la misma fuente que el currículum).

El español va en el HTML y el inglés en data-en; motor.js los cambia. Así no hay dos sitios que se
desincronicen. Con --unico escribe una versión de un solo archivo (CSS, JS, fuentes, foto y currículums
dentro) para compartir sin servidor.

Nada de aquí inventa un dato: lo que no está en su CV no está en el sitio. Lo que sí se escribió aparte es
el texto de navegación y los rótulos (Perfil, Ámbitos, «Escribirme»…)."""
import base64, hashlib, html, json, pathlib, re, sys
AQUI = pathlib.Path(__file__).resolve().parent
SITIO = AQUI / "sitio"
sys.path.insert(0, str(AQUI))
from contenido import DATOS, ES, EN   # noqa: E402
G = json.loads((AQUI / "glifos.json").read_text())
e = html.escape
def en(t): return f' data-en="{e(t, quote=True)}"'
BASE = "cv-fernanda-ramos"

# ── el monograma: la F y la R de Newsreader cursiva, enlazadas ──
MONO_VB = "-140 -1560 2320 1900"
def monograma(clase, extra=""):
    return (f'<svg class="{clase}" viewBox="{MONO_VB}" aria-hidden="true"{extra}>'
            f'<path class="tr tr--f" pathLength="1" d="{G["F"]["d"]}" transform="scale(1 -1)"/>'
            f'<path class="tr tr--r" pathLength="1" d="{G["R"]["d"]}" transform="translate(860 300) scale(1 -1)"/></svg>')

# ── una ramita botánica de trazo único (se dibuja con pathLength=1) ──
def ramita(clase, hojas=7, alto=520, semilla=3):
    import math, random
    r = random.Random(semilla)
    tallo = f"M60 {alto} C 40 {alto*.72}, 110 {alto*.52}, 70 {alto*.3} S 90 40, 120 10"
    pts = []
    for i in range(hojas):
        t = 0.14 + i * (0.8 / hojas)
        y = alto - t * (alto - 10); x = 60 + math.sin(t * 5.2) * 26 + t * 40
        lado = 1 if i % 2 else -1; L = 70 - i * 5 + r.uniform(-6, 6); ang = (-35 if lado > 0 else -145) + r.uniform(-10, 10)
        a = math.radians(ang); ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        nx, ny = -math.sin(a) * L * .32 * lado, math.cos(a) * L * .32 * lado
        mx, my = (x + ex) / 2, (y + ey) / 2
        pts.append(f'<path class="hoja" style="--h:{i}" pathLength="1" d="M{x:.1f} {y:.1f} Q {mx+nx:.1f} {my+ny:.1f} {ex:.1f} {ey:.1f} Q {mx-nx*.55:.1f} {my-ny*.55:.1f} {x:.1f} {y:.1f}"/>'
                   f'<path class="nervio" style="--h:{i}" pathLength="1" d="M{x:.1f} {y:.1f} L {(x*.25+ex*.75):.1f} {(y*.25+ey*.75):.1f}"/>')
    return (f'<svg class="{clase}" viewBox="0 0 220 {alto+10}" aria-hidden="true"><path class="tallo" pathLength="1" d="{tallo}"/>'
            + "".join(pts) + f'<circle class="yema" cx="120" cy="10" r="4.5"/></svg>')

# ── la tabla de ámbitos: cada uno con dónde lo ha llevado (sale de las viñetas de cada puesto) ──
FREYR, MINO, HERB, TRUE = "Freyr", "Mino Labs", "Herbion", "Truemed"
AMBITOS = [  # símbolo, familia, español, inglés, dónde
    ("Tc", "tramite", "Trámites ante COFEPRIS", "COFEPRIS filings", [FREYR, MINO, HERB, TRUE]),
    ("Rs", "tramite", "Registro sanitario", "Sanitary registration", [HERB, TRUE]),
    ("Ie", "tramite", "Importación y exportación", "Import and export", [FREYR, MINO, HERB]),
    ("Pu", "tramite", "Publicidad", "Advertising", [FREYR, MINO]),
    ("Me", "producto", "Medicamentos", "Medicines", [FREYR, MINO]),
    ("Dm", "producto", "Dispositivos médicos", "Medical devices", [FREYR, MINO, TRUE]),
    ("Sa", "producto", "Suplementos alimenticios", "Food supplements", [FREYR, MINO]),
    ("Co", "producto", "Cosméticos", "Cosmetics", [FREYR, MINO]),
    ("Rh", "producto", "Remedios herbolarios", "Herbal remedies", [HERB]),
    ("Fv", "vigilancia", "Farmacovigilancia", "Pharmacovigilance", [FREYR, MINO]),
    ("Tv", "vigilancia", "Tecnovigilancia", "Technovigilance", [FREYR, MINO, TRUE]),
    ("Sg", "vigilancia", "Auditoría interna y SGC", "Internal audit and QMS", [FREYR, MINO, TRUE]),
]
FAMILIAS = {"tramite": ("Trámites", "Filings"), "producto": ("Productos regulados", "Regulated products"), "vigilancia": ("Vigilancia y calidad", "Surveillance and quality")}

# la normatividad que nombra su CV, tal cual
NORMAS = ["COFEPRIS", "VUCEM", "FDA 21 CFR 820", "ISO 13485", "ISO 9001:2015", "ISO 19011", "NOM-241", "NOM-240", "NOM-073",
          "NOM-072", "NOM-248", "NOM-251", "LGS", "RIS", "BPM", "BPD", "BPAD", "LGSMP", "CEMAR", "CMN"]

HABILIDADES = [("Gestión de solicitudes", "Application filing"), ("Sometimientos regulatorios", "Regulatory submissions"),
               ("Gestión de proyectos", "Project management"), ("Asuntos regulatorios", "Regulatory affairs"),
               ("Sensibilidad intercultural", "Cultural awareness"), ("Pensamiento estratégico", "Strategic thinking"),
               ("Comunicación", "Communication"), ("Atención al detalle", "Attention to detail"), ("Cumplimiento de plazos", "Timelines")]
MCER = ["A1", "A2", "B1", "B2", "C1", "C2"]

def resaltar(t):
    for clave in ("COFEPRIS", "registro sanitario", "sanitary registration", "México y LATAM", "Mexico and LATAM", "ISO 13485", "dispositivos médicos", "medical devices"):
        t = t.replace(clave, f"<em>{clave}</em>")
    return t

def codigo_barras(texto):
    h = hashlib.sha1(texto.encode()).digest()
    barras = "".join(f'<i style="--w:{1 + b % 3}"></i>' for b in h[:22])
    return f'<span class="barras" aria-hidden="true">{barras}</span>'

def pagina():
    c = DATOS
    cv = lambda idioma, ext: f"cv/{BASE}-{idioma}.{ext}"
    tel = f'<a href="{c["tel_href"]}">{e(c["tel"])}</a>'
    correo = f'<a href="mailto:{c["correo"]}">{e(c["correo"])}</a>'

    tabla = "".join(
        f'<li class="el el--{fam} rv" style="--i:{i}"><span class="el__n" aria-label="en {len(d)} puestos">{len(d)}</span>'
        f'<b class="el__s" aria-hidden="true">{s}</b><span class="el__nom"{en(n_en)}>{e(n_es)}</span>'
        f'<span class="el__donde">{" · ".join(d)}</span></li>'
        for i, (s, fam, n_es, n_en, d) in enumerate(AMBITOS))
    leyenda = "".join(f'<li class="fam fam--{k}"><i></i><span{en(v[1])}>{v[0]}</span></li>' for k, v in FAMILIAS.items())

    def fila_normas(lista):
        h = "".join(f"<span>{n}</span><i></i>" for n in lista)
        return f'<div class="cinta__fila">{h}{h}</div>'
    cinta = fila_normas(NORMAS) + fila_normas(NORMAS[::-1])

    puestos = ""
    for p_es, p_en in zip(ES["exp"], EN["exp"]):
        anio = re.search(r"\d{4}", p_es["fechas"]).group(0)
        vinetas = "".join(f"<li{en(b)}>{e(a)}</li>" for a, b in zip(p_es["puntos"], p_en["puntos"]))
        puestos += (f'<li class="puesto rv" data-anio="{anio}"><p class="puesto__fechas"{en(p_en["fechas"])}>{e(p_es["fechas"])}</p>'
                    f'<h3 class="puesto__t"{en(p_en["puesto"])}>{e(p_es["puesto"])}</h3>'
                    f'<p class="puesto__empresa"{en(p_en["empresa"])}>{e(p_es["empresa"])}</p>'
                    f'<p class="puesto__area"{en(p_en["area"])}>{e(p_es["area"])}</p><ul class="puesto__lista">{vinetas}</ul></li>')

    certs = ""
    for (n_es, inst, f_es), (n_en, _, f_en) in zip(ES["cert"], EN["cert"]):
        paises = ""
        if "LATAM" in n_es:
            paises = '<span class="paises">' + "".join(f"<abbr title=\"{t}\">{a}</abbr>" for a, t in
                     [("MX", "México"), ("BR", "Brasil"), ("CO", "Colombia"), ("EC", "Ecuador"), ("CL", "Chile"), ("CAM", "Centroamérica")]) + "</span>"
        certs += (f'<li class="cert rv"><svg class="cert__ok" viewBox="0 0 40 40" aria-hidden="true"><circle pathLength="1" cx="20" cy="20" r="17"/>'
                  f'<path pathLength="1" d="M12.5 20.5l5 5 10-11"/></svg><div class="cert__txt"><b{en(n_en)}>{e(n_es)}</b>'
                  f'<span class="cert__inst">{e(inst)}</span>{paises}</div><p class="cert__f"{en(f_en)}>{e(f_es)}</p></li>')

    grados = "".join(
        f'<article class="grado rv"><p class="grado__anio">{f}</p><h3{en(t_en)}>{e(t_es)}</h3><p>{e(u)}</p></article>'
        for (t_es, u, f), (t_en, _, _) in zip(ES["edu"], EN["edu"]))

    def lengua(es_n, en_n, hasta, nota_es, nota_en):
        celdas = "".join(f'<li class="{"si" if k < hasta else ""}" style="--k:{k}">{n}</li>' for k, n in enumerate(MCER))
        return (f'<div class="lengua rv"><p class="lengua__cab"><b{en(en_n)}>{es_n}</b><span{en(nota_en)}>{e(nota_es)}</span></p>'
                f'<ol class="mcer" aria-label="{MCER[hasta-1]}">{celdas}</ol></div>')
    idiomas = (lengua("Inglés", "English", 6, "C2 · avanzado", "C2 · advanced")
               + lengua("Alemán", "German", 4, "B2 · intermedio · certificado Goethe-Institut", "B2 · intermediate · Goethe-Institut certificate"))

    habilidades = "".join(f"<li{en(b)}>{a}</li>" for a, b in HABILIDADES)
    nav = [("perfil", "Perfil", "Profile"), ("ambitos", "Ámbitos", "Scope"), ("trayectoria", "Trayectoria", "Experience"),
           ("certificaciones", "Certificaciones", "Certifications"), ("contacto", "Contacto", "Contact")]
    indice = "".join(f'<a href="#{i}"{en(b)}>{a}</a>' for i, a, b in nav)

    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- noindex hasta que Fernanda autorice que su página salga en buscadores -->
<meta name="robots" content="noindex">
<title>Fernanda Ramos · Asuntos Regulatorios</title>
<meta name="description" content="Fernanda Ramos, consultora en asuntos regulatorios: trámites ante COFEPRIS, registro sanitario, dispositivos médicos y sistemas de calidad en México y LATAM.">
<meta name="theme-color" content="#0B2219">
<meta property="og:title" content="Fernanda Ramos · Asuntos Regulatorios">
<meta property="og:description" content="Trámites ante COFEPRIS, registro sanitario, dispositivos médicos y sistemas de calidad en México y LATAM.">
<meta property="og:type" content="profile">
<meta property="og:image" content="https://bigtigermx.github.io/Fernanda-Berm-dez/tarjeta-social.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preload" href="fuentes/newsreader.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fuentes/instrument-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="estilo.css">
<script>(function(d){{d.classList.add('js');try{{if(sessionStorage.getItem('fr-visto'))d.classList.add('sin-telon');else sessionStorage.setItem('fr-visto','1')}}catch(e){{d.classList.add('sin-telon')}}}})(document.documentElement)</script>
</head>
<body>
<a class="saltar" href="#perfil"{en("Skip to content")}>Saltar al contenido</a>
<div class="telon" aria-hidden="true">{monograma("telon__mono")}<span class="telon__linea"></span><span class="telon__nombre">Fernanda Ramos</span></div>
<canvas class="fondo" id="fondo" aria-hidden="true"></canvas>
<svg class="enredadera" id="enredadera" aria-hidden="true"></svg>
<div class="luz" id="luz" aria-hidden="true"></div>

<header class="barra" id="barra">
  <a class="marca" href="#inicio" aria-label="Fernanda Ramos, inicio">{monograma("marca__mono")}<span class="marca__txt">Fernanda Ramos<small{en("Regulatory Affairs")}>Asuntos regulatorios</small></span></a>
  <nav class="indice" aria-label="Secciones">{indice}</nav>
  <button class="idioma" type="button" aria-label="Read in English" data-en-aria-label="Leer en español"><span>ES</span><span>EN</span></button>
</header>

<main>
<section class="portada" id="inicio">
  <div class="portada__texto">
    <p class="etiqueta ent ent--1"{en("Regulatory Affairs · COFEPRIS · Mexico and LATAM")}>Asuntos regulatorios · COFEPRIS · México y LATAM</p>
    <h1 class="nombre"><span class="ln"><span class="ln__i">Fernanda</span></span><span class="ln ln--2"><span class="ln__i"><em>Ramos</em></span></span></h1>
    <p class="bajada ent ent--2"{en("Sanitary registration and compliance for medicines, medical devices, food supplements and cosmetics.")}>Registro sanitario y cumplimiento para medicamentos, dispositivos médicos, suplementos y cosméticos.</p>
    <p class="intro ent ent--3"{en("Pharmaceutical Biotechnology Chemist with a Master’s in Quality Management. Filings before COFEPRIS, VUCEM and FDA, internal auditing, and ISO 9001 and ISO 13485 quality systems.")}>Químico Farmacéutico Biotecnólogo con maestría en Gestión de la Calidad. Trámites ante COFEPRIS, VUCEM y FDA, auditoría interna y sistemas de calidad ISO 9001 e ISO 13485.</p>
    <div class="acciones ent ent--4">
      <a class="boton boton--lleno" href="{cv('es', 'pdf')}" data-en-href="{cv('en', 'pdf')}" download><span{en("Download résumé")}>Descargar currículum</span><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v10M3.5 7.5 8 12l4.5-4.5M3 14.5h10"/></svg></a>
      <a class="boton" href="#contacto"><span{en("Get in touch")}>Escribirme</span><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8h11M9 3.5 13.5 8 9 12.5"/></svg></a>
    </div>
  </div>
  <figure class="retrato ent ent--r">
    <div class="retrato__arco"><img src="img/fernanda.webp" alt="Retrato de Fernanda Ramos" data-en-alt="Portrait of Fernanda Ramos" width="342" height="600" decoding="async"></div>
    {ramita("retrato__ramita", 6, 460, 7)}
    <figcaption class="ficha">
      <p class="ficha__cab"><span{en("Technical data sheet")}>Ficha técnica</span><span>FR</span></p>
      <dl>
        <div><dt{en("Education")}>Formación</dt><dd{en("B.Sc. Pharm. Biotech. Chem. · M. Quality Mgmt.")}>QFB · Maestría en Gestión de la Calidad</dd></div>
        <div><dt{en("Filings")}>Trámites</dt><dd>COFEPRIS · VUCEM · FDA</dd></div>
        <div><dt{en("Scope")}>Alcance</dt><dd{en("Mexico and LATAM")}>México y LATAM</dd></div>
        <div><dt{en("Languages")}>Idiomas</dt><dd{en("English C2 · German B2")}>Inglés C2 · Alemán B2</dd></div>
      </dl>
      <p class="ficha__pie">{codigo_barras("Fernanda Ramos QFB 2019 MGC 2024")}<span>QFB 2019 · MGC 2024</span></p>
    </figcaption>
  </figure>
  <ul class="cifras ent ent--5">
    <li><b data-cuenta="4">4</b><span{en("years in regulatory affairs")}>años en asuntos regulatorios</span></li>
    <li><b data-cuenta="5">5</b><span{en("product categories")}>categorías de producto</span></li>
    <li><b data-cuenta="7">7</b><span{en("certifications and diplomas")}>certificaciones y diplomados</span></li>
  </ul>
</section>

<div class="cinta" aria-hidden="true">{cinta}</div>

<section class="seccion perfil" id="perfil">
  <header class="cab-seccion"><p class="etiqueta"{en("Description")}>Descripción</p><h2 class="titulo"><span class="rv-ln"{en("Profile")}>Perfil</span></h2></header>
  <div class="perfil__grid">
    <p class="perfil__texto rv"{en(resaltar(EN["perfil"]))}>{resaltar(e(ES["perfil"]))}</p>
    <aside class="perfil__lado rv"><h3 class="mini"{en("Skills")}>Habilidades</h3><ul class="habilidades">{habilidades}</ul></aside>
    {ramita("perfil__ramita dibuja", 8, 560, 11)}
  </div>
</section>

<section class="seccion ambitos" id="ambitos">
  <canvas class="fondo-ambitos" id="fondoAmbitos" aria-hidden="true"></canvas>
  <header class="cab-seccion"><p class="etiqueta"{en("Table of scope")}>Tabla de ámbitos</p>
    <h2 class="titulo"><span class="rv-ln"{en("What she handles")}>Lo que lleva</span></h2>
    <p class="ambitos__nota rv"{en("Arranged like a periodic table. The number is how many of her positions included it.")}>Ordenado como una tabla periódica. El número es en cuántos de sus puestos lo ha llevado.</p>
    <ul class="leyenda rv">{leyenda}</ul></header>
  <ol class="tabla">{tabla}</ol>
</section>

<section class="seccion trayectoria" id="trayectoria">
  <header class="cab-seccion"><p class="etiqueta"{en("Record")}>Historial</p><h2 class="titulo"><span class="rv-ln"{en("Experience")}>Trayectoria</span></h2></header>
  <div class="historial">
    <div class="anio" aria-hidden="true"><span class="anio__caja"><span class="anio__n" id="anio">2024</span></span><span class="anio__hilo"><i id="hilo"></i></span></div>
    <ol class="puestos">{puestos}</ol>
  </div>
</section>

<section class="seccion certificaciones" id="certificaciones">
  <header class="cab-seccion"><p class="etiqueta"{en("Register of certificates")}>Registro de certificados</p><h2 class="titulo"><span class="rv-ln"{en("Certifications")}>Certificaciones</span></h2></header>
  <ol class="registro">{certs}</ol>
</section>

<section class="seccion formacion" id="formacion">
  <header class="cab-seccion"><p class="etiqueta"{en("Education")}>Formación</p><h2 class="titulo"><span class="rv-ln"{en("Education and languages")}>Formación e idiomas</span></h2></header>
  <div class="formacion__grid"><div class="grados">{grados}</div><div class="idiomas"><h3 class="mini"{en("Languages · CEFR")}>Idiomas · Marco Común Europeo</h3>{idiomas}</div></div>
</section>

<section class="contacto" id="contacto">
  {ramita("contacto__ramita dibuja", 7, 500, 5)}
  <p class="etiqueta"{en("Contact")}>Contacto</p>
  <h2 class="contacto__t"><span class="rv-ln"{en("Let’s talk.")}>Hablemos.</span></h2>
  <ul class="vias">
    <li class="via rv"><span class="via__r"{en("Email")}>Correo</span><span class="via__v">{correo}</span>
      <button class="copiar" type="button" data-copiar="{c['correo']}" data-ok="Copiado" data-en-data-ok="Copied"><span{en("Copy")}>Copiar</span></button></li>
    <li class="via rv"><span class="via__r"{en("Phone")}>Teléfono</span><span class="via__v">{tel}</span></li>
  </ul>
  <div class="descargas rv"><p class="mini"{en("Résumé")}>Currículum</p>
    <a class="ficha-dl" href="{cv('es', 'pdf')}" download><b>PDF</b><span>Español</span></a>
    <a class="ficha-dl" href="{cv('en', 'pdf')}" download><b>PDF</b><span>English</span></a>
    <a class="ficha-dl" href="{cv('es', 'docx')}" download><b>Word</b><span>Español</span></a>
    <a class="ficha-dl" href="{cv('en', 'docx')}" download><b>Word</b><span>English</span></a></div>
  <footer class="pie"><span>Fernanda Ramos</span><span{en("Regulatory Affairs")}>Asuntos regulatorios</span><a href="#inicio"{en("Back to top ↑")}>Volver arriba ↑</a></footer>
</section>
</main>
<script src="motor.js" defer></script>
</body>
</html>
"""

def favicon():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-300 -1700 2600 2200"><rect x="-300" y="-1700" width="2600" height="2200" rx="420" fill="#0B2219"/>'
            f'<path d="{G["F"]["d"]}" transform="scale(1 -1)" fill="#EEF1E6"/><path d="{G["R"]["d"]}" transform="translate(860 300) scale(1 -1)" fill="#C9A86A"/></svg>')

if __name__ == "__main__":
    h = pagina()
    (SITIO / "favicon.svg").write_text(favicon())
    huella = lambda f: hashlib.sha1((SITIO / f).read_bytes()).hexdigest()[:8]
    (SITIO / "index.html").write_text(h.replace('href="estilo.css"', f'href="estilo.css?v={huella("estilo.css")}"').replace('src="motor.js"', f'src="motor.js?v={huella("motor.js")}"'))
    print("index.html", f"{(SITIO / 'index.html').stat().st_size:,} bytes")
    if "--unico" in sys.argv:
        css = (SITIO / "estilo.css").read_text()
        css = re.sub(r'url\("(fuentes/[^"]+)"\)', lambda m: f'url("data:font/woff2;base64,{base64.b64encode((SITIO / m.group(1)).read_bytes()).decode()}")', css)
        u = h.replace('<link rel="stylesheet" href="estilo.css">', f"<style>\n{css}\n</style>")
        u = re.sub(r'<link rel="preload"[^>]+>\n', "", u).replace('<link rel="icon" href="favicon.svg" type="image/svg+xml">\n', "")
        u = u.replace('<script src="motor.js" defer></script>', f"<script>\n{(SITIO / 'motor.js').read_text()}\n</script>")
        u = u.replace('src="img/fernanda.webp"', f'src="data:image/webp;base64,{base64.b64encode((SITIO / "img/fernanda.webp").read_bytes()).decode()}"')
        MIME = {".pdf": "application/pdf", ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
        for f in sorted((SITIO / "cv").iterdir()):
            if f.suffix not in MIME: continue
            uri = f"data:{MIME[f.suffix]};base64,{base64.b64encode(f.read_bytes()).decode()}"
            u = u.replace(f'data-en-href="cv/{f.name}"', f'data-en-href="{uri}"').replace(f'href="cv/{f.name}" download', f'href="{uri}" download="{f.name}"')
            u = u.replace(f'href="cv/{f.name}" data-en-href=', f'href="{uri}" data-en-href=')
        assert 'href="cv/' not in u, "quedó un enlace a cv/ sin incrustar"
        destino = AQUI / "sitio-fernanda-ramos-un-archivo.html"; destino.write_text(u)
        print(destino.name, f"{destino.stat().st_size:,} bytes")
