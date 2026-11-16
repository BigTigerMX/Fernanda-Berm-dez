# Trazos reales de la F y la R (Newsreader cursiva, óptico 72, peso 360) para el monograma: se dibujan al entrar.
import json, pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
AQUI = pathlib.Path(__file__).resolve().parent
f = instancer.instantiateVariableFont(TTFont(AQUI / "fuentes/orig/Newsreader-Italic-VF.ttf"), {"opsz": 72, "wght": 360})
gs, cmap = f.getGlyphSet(), f.getBestCmap()
salida = {}
for letra in "FR":
    g = cmap[ord(letra)]; pen = SVGPathPen(gs); gs[g].draw(pen); b = BoundsPen(gs); gs[g].draw(b)
    salida[letra] = {"d": pen.getCommands(), "avance": gs[g].width, "caja": b.bounds}
salida["upm"] = f["head"].unitsPerEm
(AQUI / "glifos.json").write_text(json.dumps(salida)); print({k: (v["avance"], [round(x) for x in v["caja"]]) for k, v in salida.items() if k != "upm"}, salida["upm"])
