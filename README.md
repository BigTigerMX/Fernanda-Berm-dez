# Fernanda Ramos · sitio y currículum

Todo sale de su CV (`fuente/cv.pdf`, hecho en Canva). No se añadió ni un dato, cifra ni logro.

## Qué hay
- `sitio/`: la página (HTML, CSS y JS sin dependencias). Español con cambio a inglés.
- `sitio/cv/`: currículum en PDF y Word, español e inglés.
- `sitio-fernanda-ramos-un-archivo.html`: la página entera en un solo archivo, con los CV dentro.

## Cómo se rehace
1. `python3 hacer_fuentes.py`: tipografías (Newsreader, Instrument Sans, Geist Mono; licencia OFL).
2. `python3 glifos.py`: los trazos de la F y la R del monograma.
3. `python3 hacer_cv.py`: los PDF, con su revisión de lector automático (ATS).
4. `python3 hacer_docx.py`: los Word.
5. `python3 armar.py --unico`: la página y su versión de un archivo.
El texto del CV vive en `contenido.py`; la página lo toma de ahí.

## Pendiente de Fernanda (nada de esto se inventó)
- Autorizar que salga en buscadores: hoy lleva `noindex`.
- Sus dos puestos actuales se cruzan (Freyr desde jun 2024 y Mino Labs desde feb 2023, los dos «actual»). ¿Siguen los dos?
- El perfil dice «4 años»; contando desde Truemed (dic 2020) serían casi 6. Se dejó lo que ella escribió.
- Los puestos van en femenino («Coordinadora», «Consultora», «Auditora»), como ella se nombra en su perfil.
- «Universidad de Valle de México» se escribió con su nombre oficial: «del Valle».
- LinkedIn: no viene en su CV. Si lo tiene, se agrega.
- Foto: es la de su CV (207×315 px, pequeña). Con una foto de mejor resolución la portada luce más.
