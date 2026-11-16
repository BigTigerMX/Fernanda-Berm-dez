// Auditoria generica: desborde de pagina, cajas con texto recortado, contraste
// calculado (no mirado), imagenes rotas, errores de consola y conteo de reglas
// de movimiento. Se corre por ancho; el ancho es lo que destapa los recortes.
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const url = process.argv[2], w = +process.argv[3], out = process.argv[4], full = process.argv[5] === 'full';
  const lang = process.env.IDIOMA || 'es', sinJS = !!process.env.SINJS, quieto = !!process.env.QUIETO;
  const nav = await chromium.launch({ args: ['--no-sandbox'] });
  const ctx = await nav.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1, javaScriptEnabled: !sinJS, reducedMotion: quieto ? 'reduce' : 'no-preference' });
  if (!sinJS) await ctx.addInitScript(l => { try { localStorage.setItem('fr-idioma', l); } catch (e) {} }, lang);
  const pg = await ctx.newPage();
  const errs = [];
  pg.on('console', m => { if (m.type() === 'error') errs.push('CONSOLA ' + m.text()); });
  pg.on('pageerror', e => errs.push('JS ' + e.message));
  pg.on('response', r => { if (r.status() >= 400) errs.push(r.status() + ' ' + r.url()); });
  await pg.goto(url, { waitUntil: 'load', timeout: 60000 });
  await pg.waitForTimeout(3200);
  if (!sinJS) { const H = await pg.evaluate(() => document.documentElement.scrollHeight); for (let y = 0; y <= H; y += 350) { await pg.evaluate(v => window.scrollTo(0, v), y); await pg.waitForTimeout(45); } await pg.waitForTimeout(1500); }

  const r = await pg.evaluate(() => {
    const de = document.documentElement;
    const lum = c => { const v = c / 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); };
    const L = s => { const m = s.match(/[\d.]+/g); if (!m) return null; return .2126 * lum(+m[0]) + .7152 * lum(+m[1]) + .0722 * lum(+m[2]); };
    const fondoDe = el => {
      let n = el;
      while (n && n !== document.documentElement) {
        const bg = getComputedStyle(n).backgroundColor;
        const a = bg.match(/[\d.]+/g);
        if (a && (a.length < 4 || +a[3] > .5)) return bg;
        n = n.parentElement;
      }
      return getComputedStyle(document.body).backgroundColor;
    };
    // contraste de TODO nodo de texto visible
    const malos = [];
    const vistos = new Set();
    document.querySelectorAll('*').forEach(el => {
      const t = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
      if (!t) return;
      if (el.closest('[aria-hidden="true"]')) return;   // adorno, no contenido
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none') return;
      const op = +cs.opacity;
      if (op < .95) return; // los decorativos a media opacidad se auditan aparte
      const rc = el.getBoundingClientRect();
      if (!rc.width || !rc.height) return;
      const Lt = L(cs.color), Lf = L(fondoDe(el));
      if (Lt === null || Lf === null) return;
      const cr = (Math.max(Lt, Lf) + .05) / (Math.min(Lt, Lf) + .05);
      const px = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 700;
      const grande = px >= 24 || (px >= 18.66 && bold);
      const min = grande ? 3 : 4.5;
      const k = el.className + '|' + cs.color + '|' + Math.round(px);
      if (cr < min && !vistos.has(k)) { vistos.add(k); malos.push({ t: t.slice(0, 38), cls: String(el.className).slice(0, 28), px: +px.toFixed(1), col: cs.color, cr: +cr.toFixed(2), min }); }
    });
    // texto recortado: caja con overflow oculto cuyo contenido no cabe
    const recorte = [];
    document.querySelectorAll('*').forEach(el => {
      const cs = getComputedStyle(el);
      if (cs.overflow === 'visible' && cs.overflowX === 'visible' && cs.overflowY === 'visible') return;
      if (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2) {
        if (cs.overflowX === 'auto' || cs.overflowX === 'scroll' || cs.overflowY === 'auto' || cs.overflowY === 'scroll') return;
        if (el.closest('.ln, .rueda, .caratula, .carbon, .boton, .cedula')) return; // mascaras y recortes a proposito
        recorte.push({ cls: String(el.className).slice(0, 30), tag: el.tagName, sw: el.scrollWidth, cw: el.clientWidth, sh: el.scrollHeight, ch: el.clientHeight, t: (el.textContent || '').trim().slice(0, 30) });
      }
    });
    // reglas de movimiento declaradas
    let mov = 0;
    for (const ss of document.styleSheets) {
      let rs; try { rs = ss.cssRules } catch (e) { continue }
      const and = l => { for (const x of l) { if (x.style && (x.style.transition || x.style.animation || x.style.transform)) mov++; if (x.cssRules) and(x.cssRules) } };
      and(rs);
    }
    const piezas = document.querySelectorAll('.nube .pz, .nube > *');
    return {
      desborde: de.scrollWidth - de.clientWidth,
      alto: document.body.scrollHeight,
      h1: document.querySelectorAll('h1').length,
      imgRotas: [...document.images].filter(i => i.complete && i.naturalWidth === 0).length,
      imgs: document.images.length,
      reglasMovimiento: mov,
      piezasNube: piezas.length,
      piezasColocadas: [...piezas].filter(n => getComputedStyle(n).transform !== 'none').length,
      contrasteMal: malos,
      recortes: recorte.slice(0, 12),
    };
  });
  delete r.piezasNube; delete r.piezasColocadas;
  // contenido que se quedó tapado: recorte al 100 % o línea aún fuera de su máscara
  const ocultos = await pg.evaluate(() => [...document.querySelectorAll('.rv,.rv-ln,.rv-x,.mat,.ent,.ln__i,.barra')].filter(el => {
    const cs = getComputedStyle(el), r = el.getBoundingClientRect(), pr = el.parentElement.getBoundingClientRect();
    const tapado = /inset\(0px 0px 100%/.test(cs.clipPath);
    const fuera = el.classList.contains('ln__i') && r.top >= pr.bottom - 2;
    return tapado || fuera || (el.classList.contains('barra') && r.bottom <= 0);
  }).map(el => el.className.slice(0, 30)));
  console.log('ANCHO ' + w + ' ' + lang + (sinJS ? ' SINJS' : '') + (quieto ? ' QUIETO' : '') + ' html.lang=' + await pg.evaluate(() => document.documentElement.lang) + ' ocultos:' + JSON.stringify(ocultos.slice(0, 6)) + ' ' + JSON.stringify(r));
  console.log(errs.length ? 'PROBLEMAS: ' + JSON.stringify([...new Set(errs)].slice(0, 8)) : 'sin errores de consola ni 4xx');
  if (out && out !== '-') await pg.screenshot({ path: out, fullPage: full });
  await nav.close();
})();
