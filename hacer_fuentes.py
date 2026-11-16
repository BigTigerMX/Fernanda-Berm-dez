# -*- coding: utf-8 -*-
"""Tipografías de Fernanda: woff2 recortados para la web e instancias estáticas TTF para el PDF.

Newsreader (títulos, con eje óptico), Instrument Sans (texto) y Geist Mono (códigos: NOM, ISO, CFR).
Para el PDF van instancias fijas: Chromium incrusta las variables como Type 3 y un lector
automático las lee peor; las fijas salen como CID TrueType (se comprobó con el CV de Ricardo)."""
import pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

AQUI = pathlib.Path(__file__).resolve().parent
ORIG = AQUI / "fuentes" / "orig"
WEB = AQUI / "sitio" / "fuentes"; WEB.mkdir(parents=True, exist_ok=True)
PDF = AQUI / "fuentes" / "pdf"; PDF.mkdir(parents=True, exist_ok=True)
UNICODES = "U+0020-007E,U+00A0-00AC,U+00AE-00FF,U+0131,U+0152-0153,U+2013-2014,U+2018-201A,U+201C-201E,U+2022,U+2026,U+2030,U+2039-203A,U+20AC,U+2116,U+2190-2193,U+2197,U+2212,U+2713,U+00B7"

def recortar(font, destino, woff2=True):
    if "gvar" in font:
        gv = font["gvar"].variations
        for g in font.getGlyphOrder():
            try: gv[g]
            except KeyError: gv[g] = []
    opts = subset.Options(); opts.layout_features = ["*"]; opts.name_IDs = ["*"]; opts.notdef_outline = True
    opts.flavor = "woff2" if woff2 else None
    s = subset.Subsetter(opts); s.populate(unicodes=subset.parse_unicodes(UNICODES)); s.subset(font)
    font.flavor = "woff2" if woff2 else None
    font.save(str(destino)); print(f"{destino.name:40s} {destino.stat().st_size:>8,} bytes")

recortar(TTFont(ORIG / "Newsreader-VF.ttf"), WEB / "newsreader.woff2")
recortar(TTFont(ORIG / "Newsreader-Italic-VF.ttf"), WEB / "newsreader-cursiva.woff2")
recortar(instancer.instantiateVariableFont(TTFont(ORIG / "InstrumentSans-VF.ttf"), {"wdth": 100}), WEB / "instrument-sans.woff2")
recortar(TTFont(ORIG / "GeistMono-VF.ttf"), WEB / "geist-mono.woff2")

def estatica(origen, ejes, nombre, familia, estilo):
    f = instancer.instantiateVariableFont(TTFont(ORIG / origen), ejes)
    for rec in f["name"].names:
        if rec.nameID == 1: rec.string = familia
        elif rec.nameID == 2: rec.string = estilo
        elif rec.nameID == 4: rec.string = f"{familia} {estilo}"
        elif rec.nameID == 6: rec.string = f"{familia}-{estilo}".replace(" ", "")
        elif rec.nameID in (16, 17, 25): rec.string = familia if rec.nameID != 17 else estilo
    recortar(f, PDF / nombre, woff2=False)

estatica("Newsreader-VF.ttf", {"opsz": 36, "wght": 500}, "NewsreaderCV-Medium.ttf", "Newsreader CV", "Medium")
estatica("Newsreader-Italic-VF.ttf", {"opsz": 36, "wght": 400}, "NewsreaderCV-Italic.ttf", "Newsreader CV", "Italic")
for w, n in ((400, "Regular"), (500, "Medium"), (600, "SemiBold")):
    estatica("InstrumentSans-VF.ttf", {"wdth": 100, "wght": w}, f"InstrumentCV-{n}.ttf", "Instrument CV", n)
estatica("GeistMono-VF.ttf", {"wght": 400}, "GeistMonoCV-Regular.ttf", "Geist Mono CV", "Regular")
